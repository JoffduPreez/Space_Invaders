have a list of alien ships, you can check 

Collisons:
loop through list of ships, if bullet colided with one remove it from the list

Rendering:
only show ships in the list

Movement/positioning:
say i want 3 rows of ships, then after x amount of ships positon the next X amount of ships in a new row
So if rows have 10 ships, position the first 10 at the top, then the next 10 1 row down, etc
Loop through each row and adjust them at the same time

ones in the front need to shoot
if we store the ships in a 2d array then we record what indexes are at the front. For example if we have a 3 x 10 2D array. Say the ship at index 2 gets hit in row 1. Then we know the next one in the front is the ship at index 2 in row 2, because the one in the row at the front was hit

To do:
1. render enemy ships
2. add colisions/remove ships when hit
3. add enemy movement
4. add enemy shooting
5. add player health