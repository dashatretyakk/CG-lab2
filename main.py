import matplotlib.pyplot as plt

#Ініціалізація вузла KD-дерева.
class Node:
    def __init__(self, point, left=None, right=None):

        self.point = point
        self.left = left
        self.right = right

#Вставка нової точки в KD-дерево
def insert(root, point, depth=0):

    if root is None:
        return Node(point)
    
    cd = depth % 2  # Визначення осі: 0 для x, 1 для y

    if point[cd] < root.point[cd]:
        root.left = insert(root.left, point, depth + 1)
    else:
        root.right = insert(root.right, point, depth + 1)
    
    return root

#Створення KD-дерева зі списку точок.
def build_kd_tree(points):

    root = None
    for point in points:
        root = insert(root, point)
    return root

#Пошук точок у заданому діапазоні (прямокутнику)
def range_search(root, range_rect, depth=0):

    if root is None:
        return []
    
    cd = depth % 2  # Визначення осі: 0 для x, 1 для y
    xmin, ymin, xmax, ymax = range_rect
    results = []

    # Перевірка, чи знаходиться точка у прямокутнику пошуку
    if (xmin <= root.point[0] <= xmax) and (ymin <= root.point[1] <= ymax):
        results.append(root.point)
    
    # Рекурсивний пошук у лівому піддереві, якщо це необхідно
    if root.left and root.point[cd] >= (xmin if cd == 0 else ymin):
        results += range_search(root.left, range_rect, depth + 1)
    
    # Рекурсивний пошук у правому піддереві, якщо це необхідно
    if root.right and root.point[cd] <= (xmax if cd == 0 else ymax):
        results += range_search(root.right, range_rect, depth + 1)
    
    return results

def plot_kd_tree(root, xmin, xmax, ymin, ymax, depth=0, ax=None):

    if root is None:
        return
    
    cd = depth % 2  # Визначення осі: 0 для x, 1 для y
    if cd == 0:
        ax.plot([root.point[0], root.point[0]], [ymin, ymax], 'r-')  # Вертикальна лінія
        plot_kd_tree(root.left, xmin, root.point[0], ymin, ymax, depth + 1, ax)
        plot_kd_tree(root.right, root.point[0], xmax, ymin, ymax, depth + 1, ax)
    else:
        ax.plot([xmin, xmax], [root.point[1], root.point[1]], 'b-')  # Горизонтальна лінія
        plot_kd_tree(root.left, xmin, xmax, ymin, root.point[1], depth + 1, ax)
        plot_kd_tree(root.right, xmin, xmax, root.point[1], ymax, depth + 1, ax)

def visualize(points, search_rect, results):
    
    fig, ax = plt.subplots()
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    
    # Побудова KD-дерева
    root = build_kd_tree(points)
    # Візуалізація KD-дерева
    plot_kd_tree(root, 0, 10, 0, 10, ax=ax)
    
    # Візуалізація точок
    x_points, y_points = zip(*points)
    ax.plot(x_points, y_points, 'ko')  # Всі точки чорними кругами

    # Візуалізація точок, що знаходяться в діапазоні пошуку
    for result in results:
        ax.plot(result[0], result[1], 'go')  # Точки в діапазоні зеленими кругами
    
    # Візуалізація прямокутника пошуку
    xmin, ymin, xmax, ymax = search_rect
    rect = plt.Rectangle((xmin, ymin), xmax-xmin, ymax-ymin, edgecolor='green', facecolor='none')
    ax.add_patch(rect)
    
    # Друк результатів
    print("Точки, що знаходяться в діапазоні пошуку:")
    for result in results:
        print(result)
    
    plt.show()

# Приклад використання
points = [(2, 3), (5, 4), (9, 6), (4, 7), (8, 1), (7, 2)]
search_rect = (3, 2, 7, 6)
kd_tree = build_kd_tree(points)
results = range_search(kd_tree, search_rect)
visualize(points, search_rect, results)
