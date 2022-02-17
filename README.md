# Descriptive2algebraic-chess-notation-converter
This script is designed to convert from descriptive notation that we can find in old books (Spanish's one at the moment) , to Standard Algebraic Notation (SAN).

To solve the ambiguities, I use pychess python library to simulate the board and choose the right move.

## Dependencies
 ```pip install -r requirements.txt```

## Usage
### Convert individual file
```python translator.py```

it will ask (via FileDialog windows popup) to select a file. There is a folder called *sample input files* with some examples. Let's choose *Legal mate.txt* 
```
1. P4R P4R
2. A4A P3D
3. C3AR C3AD
4. C3A A5C
5. CxP AxD
6. AxP R2R
7. C5D ++
```
Then it will ask (via saveDialog windows popup) for a file with extension *.pgn. Let's write *Legal mate.pgn*

The program will generate a file called *Legal mate.pgn* with the following code (*it is a default header, needed to be uploaded in the right way to software like Arena or PyChess):

```
[Event "?"]
[Site "?"]
[Site "?"]
[Date "????.??.??"]
[Round "?"]
[White "?"]
[Black "?"]
[Result "?-?"]

1. e4 e5
2. Bc4 d6
3. Nf3 Nc6
4. Nc3 Bg4
5. Nxe5 Bxd1
6. Bxf7+ Ke7
7. Nd5 ++
```

This file can be pasted or loaded in chess programs like *chess.com*, *Pychess* or *Arena*.

### Bulk Convert 
There is another file that can convert serveral files inside a folder. That's called *batch_conversion.py*

```batch_conversion.py```

And we select a folder with files in descriptive format. Then we select output folder and script will do the job, generating a pgn file for each descriptive source file.







