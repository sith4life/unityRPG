import pygame
import tile
import heap

def get_distance(a : tile.Tile, b : tile.Tile):
    """Calculate the heuristic distance between two points."""
    distX = abs(a.grid_posX() - b.grid_posX() )
    distY = abs(a.grid_posY()  - b.grid_posY() )
    if distX > distY:
        distance = 14 * distY + 10 * (distX - distY)
    else:
        distance = 14 * distX + 10 * (distY - distX)
    return distance

def find_path(start : tile.Tile, goal : tile.Tile, map : r"game_manager"):
    """Perform A* pathfinding from start to goal."""
    
    open_list = heap.Heap()
    open_list.add(start)
    #open_list = [start]
    closed_list = []
    while open_list.current_item_count > 0:
        current_tile = open_list.remove_first()
        # for i in open_list:
        #     if i.f_cost() < current_tile.f_cost() or (i.f_cost() == current_tile.f_cost() and i.h_cost < current_tile.h_cost):
        #         current_tile = i
        # open_list.remove(current_tile)
        closed_list.append(current_tile)

        if current_tile == goal:
            path = []
            while current_tile != start:
                path.append(current_tile)
                current_tile = current_tile.parent
            path.reverse()
            return path
        current_tile.neighbours = map.get_neighbours(current_tile)
        for neighbour in current_tile.neighbours:
            if neighbour in closed_list or neighbour.impassable:
                continue
            new_cost = current_tile.g_cost + get_distance(current_tile, neighbour) + neighbour.movement_penalty
            if new_cost < neighbour.g_cost or neighbour not in open_list:
                neighbour.g_cost = new_cost
                neighbour.h_cost = get_distance(neighbour, goal)
                neighbour.parent = current_tile
                if neighbour not in open_list:
                    open_list.add(neighbour)
                else:
                    open_list.update(neighbour)
        

