# multi-drone-quiz
This program chose to calculate along columns first, then calculate along rows. The results should be the same in reverse.

## Compute vertical distance

- For every column
  1. Find all obstacles located in the current column. Form a new list `ob_c`.
      
      ```python
      ob_c = [i[0] for i in obstacle_list if i[1] == c]
      ```
  2. Compute the intersections `its_c` of obstacles in `ob_c`.
      
      ```python
      its = [(ob[i]+ob[i+1])/2 for i in range(len(ob)-1)]
      its.append(C)
      ```
  3. Locate the nearest obstacle for every cell in the column based on `its_c`. Compute the vertical distance `dis_c`.
      
      ```python
      if dis[0,i] == 0:
         continue
      if i > its[a]:
         a += 1
      dis[0,i] = abs(i - ob[a])
      ```
- Form vertical distance map `map_1` by merging all `dis_c`` for every column.
   
   ```python
   map_1 = np.append(map_1, dis_c.T,axis=1)
   ```


## Compute the final distance by calculating horizontally

- For every row
   1. Compute the lower envelope `low_env` of every cell in the current row. Get vertical distances for this row `dis_r` from `map_1`. Use `dis_r` as *original function*.
      
      ```python
      l = 0
      low_env = np.array([-(2*N)**2,(2*N)**2],dtype=float)
      for i in range(1,N):
         ist = ((i**2 + map_1[r,i]) - (l**2 +map_1[r,l]))/(2*(i-l))
         if ist <= low_env[l]:
               l-=1
               i-=1
         else:
               l+=1
               low_env[l] = ist
               low_env = np.append(low_env,(2*N)**2)
      low_env = np. floor(low_env)
      ```

   2. Locate the nearest obstacle for every cell based on the `low_env`, Compute the final distance `dis_c`.
      
      ```python
      for i in range(0,N):
         while low_env[l+1] < i :
            l+=1
         map_2[r,i] = (l-i)**2 + map_1[r,l]
      ```
