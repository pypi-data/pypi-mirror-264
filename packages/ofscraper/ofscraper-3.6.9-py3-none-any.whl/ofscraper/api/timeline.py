r"""
                                                             
  _____/ ____\______ ________________    ____   ___________ 
 /  _ \   __\/  ___// ___\_  __ \__  \  /  _ \_/ __ \_  __ \
(  <_> )  |  \___ \\  \___|  | \// __ \(  <_> )  ___/|  | \/
 \____/|__| /____  >\___  >__|  (____  /\____/ \___  >__|   
                 \/     \/           \/            \/         
"""
import asyncio
import contextvars
import logging
import math
from concurrent.futures import ThreadPoolExecutor

import arrow
from diskcache import Cache
from rich.console import Group
from rich.live import Live
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.style import Style
from tenacity import retry, retry_if_not_exception_type, stop_after_attempt, wait_random

import ofscraper.classes.sessionbuilder as sessionbuilder
import ofscraper.constants as constants
import ofscraper.db.operations as operations
import ofscraper.utils.args as args_
import ofscraper.utils.config as config_
import ofscraper.utils.console as console
from ofscraper.classes.semaphoreDelayed import semaphoreDelayed
from ofscraper.utils.run_async import run

from ..utils.paths import getcachepath

log = logging.getLogger("shared")
attempt = contextvars.ContextVar("attempt")

sem = semaphoreDelayed(constants.MAX_SEMAPHORE)


@retry(
    retry=retry_if_not_exception_type(KeyboardInterrupt),
    stop=stop_after_attempt(constants.NUM_TRIES),
    wait=wait_random(min=constants.OF_MIN, max=constants.OF_MAX),
    reraise=True,
)
async def scrape_timeline_posts(
    c, model_id, progress, timestamp=None, required_ids=None
) -> list:
    global new_tasks
    global sem
    posts = None
    attempt.set(attempt.get(0) + 1)

    if timestamp and (
        float(timestamp) > (args_.getargs().before or arrow.now()).float_timestamp
    ):
        return []
    if timestamp:
        log.debug(arrow.get(math.trunc(float(timestamp))))
        ep = constants.timelineNextEP
        url = ep.format(model_id, str(timestamp))
    else:
        ep = constants.timelineEP
        url = ep.format(model_id)
    log.debug(url)
    try:
        task = progress.add_task(
            f"Attempt {attempt.get()}/{constants.NUM_TRIES}: Timestamp -> {arrow.get(math.trunc(float(timestamp))) if timestamp!=None  else 'initial'}",
            visible=True,
        )
        await sem.acquire()
        async with c.requests(url=url)() as r:
            if r.ok:
                progress.remove_task(task)
                posts = (await r.json_())["list"]
                log_id = f"timestamp:{arrow.get(math.trunc(float(timestamp))) if timestamp!=None  else 'initial'}"
                if not posts:
                    posts = []
                if len(posts) == 0:
                    log.debug(f"{log_id} -> number of post found 0")

                elif len(posts) > 0:
                    log.debug(f"{log_id} -> number of post found {len(posts)}")
                    log.debug(
                        f"{log_id} -> first date {posts[0].get('createdAt') or posts[0].get('postedAt')}"
                    )
                    log.debug(
                        f"{log_id} -> last date {posts[-1].get('createdAt') or posts[-1].get('postedAt')}"
                    )
                    log.debug(
                        f"{log_id} -> found postids {list(map(lambda x:x.get('id'),posts))}"
                    )
                    log.trace(
                        "{log_id} -> post raw {posts}".format(
                            log_id=log_id,
                            posts="\n\n".join(
                                list(
                                    map(
                                        lambda x: f"scrapeinfo timeline: {str(x)}",
                                        posts,
                                    )
                                )
                            ),
                        )
                    )
                    if required_ids == None:
                        attempt.set(0)
                        new_tasks.append(
                            asyncio.create_task(
                                scrape_timeline_posts(
                                    c,
                                    model_id,
                                    progress,
                                    timestamp=posts[-1]["postedAtPrecise"],
                                )
                            )
                        )
                    else:
                        [
                            required_ids.discard(float(ele["postedAtPrecise"]))
                            for ele in posts
                        ]
                        if len(required_ids) > 0 and float((timestamp) or 0) <= max(
                            required_ids
                        ):
                            attempt.set(0)
                            new_tasks.append(
                                asyncio.create_task(
                                    scrape_timeline_posts(
                                        c,
                                        model_id,
                                        progress,
                                        timestamp=posts[-1]["postedAtPrecise"],
                                        required_ids=required_ids,
                                    )
                                )
                            )
            else:
                log.debug(f"[bold]timeline response status code:[/bold]{r.status}")
                log.debug(f"[bold]timeline response:[/bold] {await r.text_()}")
                log.debug(f"[bold]timeline headers:[/bold] {r.headers}")
                progress.remove_task(task)
                r.raise_for_status()
    except Exception as E:
        raise E
    finally:
        sem.release()
    return posts


@run
async def get_timeline_media(model_id, username, forced_after=None, rescan=None):
    with ThreadPoolExecutor(max_workers=20) as executor:
        asyncio.get_event_loop().set_default_executor(executor)
        overall_progress = Progress(
            SpinnerColumn(style=Style(color="blue")),
            TextColumn("Getting timeline media...\n{task.description}"),
        )
        job_progress = Progress("{task.description}")
        progress_group = Group(overall_progress, Panel(Group(job_progress)))

        global tasks
        global new_tasks
        tasks = []
        new_tasks = []
        min_posts = 50
        responseArray = []
        page_count = 0
        if not args_.getargs().no_cache:
            oldtimeline = operations.get_timeline_postdates(
                model_id=model_id, username=username
            )
        else:
            oldtimeline = []
        log.trace(
            "oldtimeline {posts}".format(
                posts="\n\n".join(
                    list(map(lambda x: f"oldtimeline: {str(x)}", oldtimeline))
                )
            )
        )
        log.debug(f"[bold]Timeline Cache[/bold] {len(oldtimeline)} found")
        oldtimeline = list(filter(lambda x: x != None, oldtimeline))
        postedAtArray = sorted(oldtimeline)
        after = after = 0 if rescan else forced_after or get_after(model_id, username)

        log.info(
            f"""
Setting initial timeline scan date for {username} to {arrow.get(after).format('YYYY.MM.DD')}
[yellow]Hint: append ' --after 2000' to command to force scan of all timeline posts + download of new files only[/yellow]
[yellow]Hint: append ' --after 2000 --dupe' to command to force scan of all timeline posts + download/re-download of all files[/yellow]

                """
        )
        filteredArray = list(filter(lambda x: x >= after, postedAtArray))
        with Live(
            progress_group, refresh_per_second=5, console=console.get_shared_console()
        ):
            async with sessionbuilder.sessionBuilder() as c:
                if len(filteredArray) >= min_posts + 1:
                    splitArrays = [
                        filteredArray[i : i + min_posts]
                        for i in range(0, len(filteredArray), min_posts)
                    ]
                    # use the previous split for timestamp
                    if len(filteredArray) >= (min_posts * 2) + 1:
                        tasks.append(
                            asyncio.create_task(
                                scrape_timeline_posts(
                                    c,
                                    model_id,
                                    job_progress,
                                    required_ids=set(splitArrays[0]),
                                    timestamp=after,
                                )
                            )
                        )
                        [
                            tasks.append(
                                asyncio.create_task(
                                    scrape_timeline_posts(
                                        c,
                                        model_id,
                                        job_progress,
                                        required_ids=set(splitArrays[i]),
                                        timestamp=splitArrays[i - 1][-1],
                                    )
                                )
                            )
                            for i in range(1, len(splitArrays) - 1)
                        ]
                        # keeping grabbing until nothing left
                        tasks.append(
                            asyncio.create_task(
                                scrape_timeline_posts(
                                    c,
                                    model_id,
                                    job_progress,
                                    timestamp=splitArrays[-2][-1],
                                )
                            )
                        )
                    else:
                        tasks.append(
                            asyncio.create_task(
                                scrape_timeline_posts(
                                    c,
                                    model_id,
                                    job_progress,
                                    timestamp=splitArrays[-1][-1],
                                )
                            )
                        )

                else:
                    tasks.append(
                        asyncio.create_task(
                            scrape_timeline_posts(
                                c, model_id, job_progress, timestamp=after
                            )
                        )
                    )
                page_task = overall_progress.add_task(
                    f" Pages Progress: {page_count}", visible=True
                )
                while tasks:
                    done, pending = await asyncio.wait(
                        tasks, return_when=asyncio.FIRST_COMPLETED
                    )
                    for result in done:
                        try:
                            result = await result
                        except Exception as E:
                            log.debug(E)
                            continue
                        page_count = page_count + 1
                        overall_progress.update(
                            page_task, description=f"Pages Progress: {page_count}"
                        )
                        responseArray.extend(result)
                    tasks = list(pending)
                    tasks.extend(new_tasks)
                    new_tasks = []
                overall_progress.remove_task(page_task)

        unduped = {}
        log.debug(f"[bold]Timeline Count with Dupes[/bold] {len(responseArray)} found")
        for post in responseArray:
            id = post["id"]
            if unduped.get(id):
                continue
            unduped[id] = post

        log.trace(f"timeline dupeset postids {list(unduped.keys())}")
        log.trace(
            "post raw unduped {posts}".format(
                posts="\n\n".join(
                    list(map(lambda x: f"undupedinfo timeline: {str(x)}", unduped))
                )
            )
        )
        log.debug(f"[bold]Timeline Count without Dupes[/bold] {len(unduped)} found")
        return list(unduped.values())


def get_individual_post(id, c=None):
    with c.requests(constants.INDVIDUAL_TIMELINE.format(id))() as r:
        if r.ok:
            log.trace(f"post raw individual {r.json()}")
            return r.json()
        else:
            log.debug(f"[bold]individual post response status code:[/bold]{r.status}")
            log.debug(f"[bold]individual post response:[/bold] {r.text_()}")
            log.debug(f"[bold]individual post headers:[/bold] {r.headers}")


def get_after(model_id, username):
    cache = Cache(getcachepath(), disk=config_.get_cache_mode(config_.read_config()))
    if args_.getargs().after:
        return args_.getargs().after.float_timestamp
    curr = operations.get_timeline_media(model_id=model_id, username=username)
    if cache.get(f"{model_id}_scrape_timeline"):
        log.debug(
            "Used after previously scraping entire timeline to make sure content is not missing"
        )
        return 0
    elif len(curr) == 0:
        log.debug("Setting date to zero because database is empty")
        return 0
    missing_items = list(filter(lambda x: x[10] != 1, curr))
    missing_items = list(sorted(missing_items, key=lambda x: arrow.get(x[12])))
    if len(missing_items) == 0:
        log.debug("Using last db date because,all downloads in db marked as downloaded")
        return (
            operations.get_last_timeline_date(model_id=model_id, username=username)
            - 1000
        )
    else:
        log.debug(
            f"Setting date slightly before earliest missing item\nbecause {len(missing_items)} posts in db are marked as undownloaded"
        )
        return arrow.get(missing_items[0][-1]).float_timestamp - 1000
