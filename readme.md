# Lemona
'Lemona' is a simple interpreter language using python
```
lemona support variable declaration using 'LET' keyword:
```

```
LET X = 10.
LET A = 3.14, B = "Lemona".
```

```
lemona support selection using 'IF' statement:
```

```
IF 10 > 2 AND 10 >+ 3 OR 10 <= 0:
  DO SOME THING HERE
END
```

```
lemona support LOOPING using 'FROM-TO' statement:
```

```
FROM 1 TO 5:
  DO SOME THING HERE
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
