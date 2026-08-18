# Algorithmie

Ce fichier permet de noter les différents algorithmes rencontrés lors des problèmes résolus, afin de pouvoir les réutiliser lors d'un nouveau problème.

## Heapq - Heap queue algorithm

Une heap est une structure de données permettant de gérer efficacement une file de priorité.

Propriétés d'une min-heap :
- Le plus petit élément est toujours à la première position (heap[0]).
- C'est un arbre binaire où chaque parent est inférieur ou égal à ses enfants.
- Les enfants entre eux n'ont pas besoin d'être triés.

```text
          1
        /   \
       3     2
      / \   / \
     7   5 8   4
```

Complexités
- Regarder le plus petit élement: O(1)
- Retirer le plus petit élement: O(log(n))
    - On pourrait penser que c'est une compléxité en O(1) comme on pop simplement le premier element. Mais une fois pop il faut recontruire l'arbre. La méthodo est on prends le dernier element de la queue et on l'ajoute au début de l'arbre. Seulement si il ne respecte pas les conditions il faut le redescendre d'un étage, jusqu'a ce qu'il soit au bon étage. Or on a h étages (h=log(n)) comme cc'est un arbre binaire
- Créer une heapq depuis une liste: O(n)
    - On construit la heap du bas vers le haut.
    - La majorité des éléments sont proches des feuilles et ne peuvent descendre que de quelques niveaux. Le coût total est donc O(n).
- Ajout d'un élement: O(log(n))
    - L'élément est ajouté à la fin puis remonte jusqu'à respecter la propriété de heap.

### Utilisation en python

```python
import heapq
heap = [5, 2, 8, 1, 3]
heapq.heapify(heap) # compléxité O(n)

heapq.heappush(heap) # compléxité O(log n)

heapq.heappop(heap) # compléxité O(log n)
```

### Pourquoi utiliser une heapq

Utile lorsqu'on effectue beaucoup d'ajouts et de retraits du minimum.

Avec une liste triée :
- ajouter un élément au bon endroit : O(n)
- retirer le minimum : O(1) si on retire à la fin

Avec une heap :
- ajouter un élément : O(log n)
- retirer le minimum : O(log n)
- regarder le minimum : O(1)
