import tile
class Heap:
    def __init__(self):
        """Initialize the heap with an optional list of items."""
        self.items = []
        self.current_item_count = 0

    def __len__(self):
        """Return the number of items in the heap."""
        return self.current_item_count
    
    def __contains__(self, item):
        """Check if an item is in the heap."""
        return item in self.items
        #return True if item == self.items[item.heap_index] else False
    
    def update(self, item):
        self.sort_up(item)

    def add(self,item):
        """Add an item to the heap."""
        item.heap_index = self.current_item_count
        self.items.append(item)
        self.sort_up(item)
        self.current_item_count += 1
    
    def compare_priority(self,x,y):
        return x.compare_to(y)

    def swap_items(self,item_a, item_b):
        self.items[item_a.heap_index] = item_b
        self.items[item_b.heap_index] = item_a

        t = item_a.heap_index
        item_a.heap_index = item_b.heap_index
        item_b.heap_index = t

    def remove_first(self):
        """Remove and return the item with the lowest f_cost."""
        if self.current_item_count == 0:
            return None

        first_item = self.items[0]
        self.current_item_count -= 1

        if self.current_item_count > 0:
            self.items[0] = self.items[self.current_item_count] 
            self.items[0].heap_index = 0
            self.items.pop()
            self.sort_down(self.items[0])
        else:
            self.items.pop()
        return first_item

    def sort_up(self,item):
        """Sort the item up in the heap."""
        parent_index = (item.heap_index - 1) // 2
        while item.heap_index > 0 and self.compare_priority(item,self.items[parent_index]) < 0:
            self.swap_items(item,self.items[parent_index])
            parent_index = (item.heap_index - 1) // 2

    def sort_down(self,item):
        """Sort the item down in the heap."""
        while True:
            n = item.heap_index
            child_left_index = n * 2 + 1
            child_right_index = n * 2 + 2
            swap_index = None
            if child_left_index >= self.current_item_count:
                return
            else:
                swap_index = child_left_index
                if child_right_index < self.current_item_count:
                    if self.compare_priority(self.items[child_right_index], self.items[child_left_index]):
                        swap_index = child_right_index
                if self.compare_priority(item,self.items[swap_index]):
                    self.swap_items(item,self.items[swap_index])
                else:
                    return

if __name__ == "__main__":
    # Example usage
    heap = Heap()
    tile1 = tile.Tile((50, 50), 50, (255, 255, 255))
    tile1.g_cost = 10
    tile1.h_cost = 20
    tile2 = tile.Tile((17, 1), 50, (255, 255, 255))
    tile2.g_cost = 5
    tile2.h_cost = 15
    tile3 = tile.Tile((1, 2), 50, (255, 255, 255))
    tile3.g_cost = 2
    tile3.h_cost = 10

    heap.add(tile1)
    heap.add(tile2)
    heap.add(tile3)
    print([(x.position, x) for x in heap.items])  # Output: 2

    print(heap.remove_first().position)
    print([(x.position, x) for x in heap.items])  # Output: 2