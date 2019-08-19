import random

cards = [n+1 for n in range(20)]

print(f"set: {cards}")

random.shuffle(cards)

print(f"shuffeled: {cards}")

def quicksort(elements):
	if len(elements) <= 1:
		return elements
	pivotIndex = random.choice(range(len(elements)))
	pivot = elements[pivotIndex]

	smaller = []
	bigger = []

	for i, el in enumerate(elements):
		if i != pivotIndex:
			if el < pivot:
				smaller.append(el)
			else:
				bigger.append(el)

	smallerSorted = quicksort(smaller)
	biggerSorted = quicksort(bigger)

	elementsSorted = smallerSorted + [pivot] + biggerSorted
	return elementsSorted





def mergesort(eles):
	if len(eles) <= 1:
		return eles
	splitIndex = len(eles)//2
	left = eles[:splitIndex]
	right = eles[splitIndex:]
	leftSorted = mergesort(left)
	rightSorted = mergesort(right)

	final = []
	while (len(leftSorted) > 0) and (len(rightSorted) > 0):
		air = 0
		if leftSorted[0] > rightSorted[0]:
			air = rightSorted.pop(0)
		else:
			air = leftSorted.pop(0)
		final.append(air)

	return final + leftSorted + rightSorted


print(f"sorted: {quicksort(cards)}")