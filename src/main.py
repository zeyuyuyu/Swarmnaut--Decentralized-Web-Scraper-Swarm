import asyncio
import random
from typing import List, Dict

class ScraperNode:
    def __init__(self, node_id: str, capacity: int):
        self.node_id = node_id
        self.capacity = capacity
        self.tasks = []

    def add_task(self, task: 'ScrapeTask'):
        if len(self.tasks) < self.capacity:
            self.tasks.append(task)
            return True
        return False

    async def process_tasks(self):
        while self.tasks:
            task = self.tasks.pop(0)
            await task.scrape()

class ScrapeTask:
    def __init__(self, url: str):
        self.url = url

    async def scrape(self):
        # Implement scraping logic here
        await asyncio.sleep(random.uniform(1, 5))
        print(f'Scraped {self.url}')

class SwarmCoordinator:
    def __init__(self, nodes: List[ScraperNode]):
        self.nodes = nodes
        self.task_queue: List[ScrapeTask] = []

    def add_task(self, task: ScrapeTask):
        self.task_queue.append(task)

    async def schedule_tasks(self):
        while self.task_queue:
            task = self.task_queue.pop(0)
            assigned = False
            for node in self.nodes:
                if node.add_task(task):
                    assigned = True
                    break
            if not assigned:
                self.task_queue.append(task)
            await asyncio.sleep(0.1)

    async def run(self):
        await asyncio.gather(
            *[node.process_tasks() for node in self.nodes],
            self.schedule_tasks()
        )

async def main():
    nodes = [
        ScraperNode(f'node_{i}', capacity=3) for i in range(5)
    ]
    coordinator = SwarmCoordinator(nodes)

    for url in ['https://example.com', 'https://google.com', 'https://github.com', 'https://openai.com', 'https://swarmnaut.io']:
        coordinator.add_task(ScrapeTask(url))

    await coordinator.run()

if __name__ == '__main__':
    asyncio.run(main())