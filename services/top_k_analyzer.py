import heapq


class TopKAnalyzer:

    @staticmethod
    def top_k(items, metric_function, k=5):

        if k <= 0:
            return []

        heap = []

        for index, item in enumerate(items):

            metric = metric_function(item)

            # index prevents Python from trying to compare
            # dictionaries when two metrics are equal.
            entry = (metric, index, item)

            if len(heap) < k:

                heapq.heappush(
                    heap,
                    entry
                )

            elif metric > heap[0][0]:

                heapq.heapreplace(
                    heap,
                    entry
                )

        heap.sort(
            key=lambda x: x[0],
            reverse=True
        )

        return [
            item
            for metric, index, item in heap
        ]