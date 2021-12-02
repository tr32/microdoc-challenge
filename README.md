# MicroDoc-Coding-Challenge from 29.11.2021

Coding Challenge:  
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------  
Given an arbitrary huge text file (expect multiple Terabyte TB) with one number in each line, e.g.  

3  
67  
84,000  
78965755,43  
8.0  

implement an algorithm that finds the exact median of all numbers (no approximation) and print the result on std out.  
The file should be given to the application via argument at startup on the command line.  
Please provide the source code and a description how to build the program. The usage of existing libraries, frameworks, or external systems is prohibited.  
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------  

## Approach / Lösungsansatz

Um den Median zu berechnen, müssen die Werte in der Datei sortiert werden.
Da es sich um mehrere Terabyte an Daten handelt, können nicht alle Werte auf einmal in den Speicher geladen werden.
Ein Lösungsansatz wäre hierbei, die Anzahl Zahlen bzw. Zeilen zu ermitteln und 
dann die Datei in Frames aufzuteilen, jedes Frame wird sortiert und anschließend 
durch merge sort alles Frames zusammengesetzt werden, 
dann kann man den Median ermitteln.
Um das Sortieren der einzelnen Frames zu beschleunigen, 
kann man multiprocessing bzw. multithreading benutzen.
