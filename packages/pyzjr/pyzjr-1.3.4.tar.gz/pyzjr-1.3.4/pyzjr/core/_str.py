__all__=["Letterlabels", "Sorting"]

alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
uppercase_alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

def Letterlabels(capital=False):
    """字母标签"""
    return uppercase_alphabet if capital else alphabet

class Sorting():
    """排序算法"""
    def insertion_sort(self, arr):
        """直接插入排序"""
        n = len(arr)
        for i in range(1, n):
            key = arr[i]
            j = i - 1
            while j >= 0 and arr[j] > key:
                arr[j + 1] = arr[j]
                j -= 1
            arr[j + 1] = key
            print(arr)

    def quick_sort(self, arr, low, high):
        """快速排序"""
        if low < high:
            pivot_index = self.partition(arr, low, high)
            print(arr)
            self.quick_sort(arr, low, pivot_index - 1)
            self.quick_sort(arr, pivot_index + 1, high)

    def partition(self, arr, low, high):
        pivot = arr[high]
        i = low - 1
        for j in range(low, high):
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        return i + 1

    def bubble_sort(self, arr):
        """冒泡排序"""
        n = len(arr)
        for i in range(n - 1):
            for j in range(n - 1 - i):
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
            print(arr)

    def selection_sort(self, arr):
        """直接选择排序"""
        n = len(arr)
        for i in range(n - 1):
            min_index = i
            for j in range(i + 1, n):
                if arr[j] < arr[min_index]:
                    min_index = j
            arr[i], arr[min_index] = arr[min_index], arr[i]
            print(arr)
