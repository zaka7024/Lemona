# Lemona
'Lemona' is a simple interpreter language using python
```
lemona support variable and list declarations using 'LET' keyword:
```

```
LET X = 10.
LET B = "Lemona".
LET names = ["AHMAD", "Abed", "Ibrahim"].
names[1] = "ZAKA7024"
```

```
lemona support selection using 'IF' statement:
```

```
IF 10 > 2 AND 10 >= 3 OR 10 <= 0:
  DO SOME THING HERE
END
```

```
lemona support LOOPING using 'FROM-TO' statement:
```

```
LET x = [2, 4, 6, 8, 10].
LET INDEX = 1.
FROM 1 TO 6:
  x[INDEX] = 0
  INDEX = INDEX - 1
END
```
```
LET X = 0.
FROM 1 TO 10 STEP 2:
  X = X + 1
END
```

```
LET X = 10.
FROM 1 TO 5:
  CONTINUE
  X = 0
END
```

```
lemona support LOOPING using 'WHILE' statement:
```

```
LET I = 10.
WHILE I > 0:
  I = I - 1
END
```

