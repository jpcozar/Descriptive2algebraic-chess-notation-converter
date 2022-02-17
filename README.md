# Descriptive2algebraic-chess-notation-converter
The script **translator.py** is designed to convert from descriptive notation that we can find in old chess books (Spanish's one at the moment) , to Standard Algebraic Notation (SAN).

To solve the ambiguities, I use pychess python library to simulate the board and choose the right move.

There is another script, called **batch_conversion.py** that can convert several files in a folder to SAN notation.

## Dependencies
 ```pip install -r requirements.txt```

## Usage
### Convert individual file
```python translator.py```

it will ask (via *FileDialog* windows popup) to select a file. There is a folder called *sample input files* with some examples. Let's choose *Legal mate.txt* file
```
1. P4R P4R
2. A4A P3D
3. C3AR C3AD
4. C3A A5C
5. CxP AxD
6. AxP R2R
7. C5D ++
```
Then it will ask (via *saveDialog* windows popup) for a file with **.pgn** extension. Let's write *Legal mate.pgn*

The program will generate a file called *Legal mate.pgn* with the following code (*it is a default header, needed to be able to upload it to software like Arena or PyChess*.):

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

This file can be pasted or loaded in chess software like *chess.com*, *Pychess* or *Arena*.

we can just paste in <https://chess.com/analysis> this part:
```
1. e4 e5
2. Bc4 d6
3. Nf3 Nc6
4. Nc3 Bg4
5. Nxe5 Bxd1
6. Bxf7+ Ke7
7. Nd5 ++
`````

### Bulk Convert 
There is another file that can convert several descrtiptive format files inside a folder. That's called *batch_conversion.py*

```batch_conversion.py```

And it will ask for a folder with files in descriptive format inside. 
Then it will ask for an output folder and script will do the job, generating a pgn file for each descriptive source file, giving a final message about how much files were converted.

# Notes
Most examples are taken from the book "Celadas en Ajedrez" from Alexei Pavlovich Sokolsky.

This is a beta version yet!!!
Comments are welcomed








