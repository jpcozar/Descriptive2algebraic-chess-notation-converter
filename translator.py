'''This is a python program to translate from Spanish descriptive notation \
 to Standard algebraic notation'''
'''Author: Javier Polo Cózar'''
'''Date: February 2022'''

# Module dependencies

import os                 # For paths and so 
from os.path import join 
from xml.dom.minidom import CharacterData                 # Need for working with paths
import chess              # Library for chess software simulation
import tkinter.filedialog # Needed to fileDailog for choose input file
import sys                 # for arguments

# Spanish list of pieces in descriptive notation
Spapieces=["R","D","T","A","C","P"]

# Standard (English) list of pieces in algebraic notation
pieces=["K","Q","R","B","N","P"]

# Spanish list of cols in descriptive notation
DescColumns=["TD","CD","AD","D","R","AR","CR","TR"]

# Standard list of cols in algebraic notation
AlgColumns=["a","b","c","d","e","f","g","h"]


# Chess board for doing chess game simulation
board=chess.Board()


def printDefaultBoard():
    print("=============")
    print("DEFAULT BOARD")
    print("=============")
    print(board)
    print("=============\n")



def convert_list_col_desc_alg(listOfColumns):
    listOfColumnsAlg=[]
    for elemento in listOfColumns:
        listOfColumnsAlg.append(AlgColumns[DescColumns.index(elemento)])
    return listOfColumnsAlg


def check_colambiguities(column):
    """Function for detecting ambiguity in columns. 
    If will return either a col if there's no ambiguity (string) or a list of columns (list)
    Parameters:
    column (char): destination column of next move

    Returns:
    a string or a list of strings: column or possible columns
    """
    listofCols=[]
    if (column=='A' or column=='T' or column=='C'): # There are ambiguities just in A,T,C columns
        for element in DescColumns:
            if column in element:
                listofCols.append(element)
        return listofCols
    else:
        return column 


def check_capture(grabber,captured,listofCaptures,whiteT):
    """ Function for get right capture when there is ambiguity
    Parameters:
    grabber (char): piece who captures
    captured (char): piece who is captured

    Returns:
    element (string): a element with next move which is a capture
    """
    list_captures=[] # listad de casillas de captura
  
    

    if (grabber=="P" and captured=="P"): # Pawns are involved: lower first initial
        for element in listofCaptures:
            if (element[0].islower() and element[2].islower()):
                print ("Capture: " + element)
                return(element)
    else:
    
    # Nos quedamos con las posibles piezas capturadas (parte a la derecha del 'x')
    
        for capture in listofCaptures:
            captured_pieces=capture.split('x')
            list_captures.append((captured_pieces[1]))
                
        print (list_captures)

        for capture in list_captures:
            piece_captured=board.piece_at(chess.parse_square((capture[0:2]))) #para evitar los f7+
            if (not piece_captured is None):
                if (piece_captured.symbol().upper()==captured): # para evitar las negras en minusculas
                    for element in listofCaptures:
                        if capture in element:
                            if (grabber != "P"):
                                return(grabber+"x"+capture)
                            else: 
                                return(element)

#Function to translate Spanish to English piece
def Spa2EngPiece(piece):
    return pieces[Spapieces.index(piece)]

# Function to translate Desc2Alg col

def Desc2AlgCol(col):
    return AlgColumns[DescColumns.index(col)]


def capture(move,whiteT):
    """ Function to do a capture 
    Parameters:
    move (string): the next move in descriptive notation, which is a capture, for example PxP, 
    PDxA or PxAD
    
    Returns:
    move (string): the move in algebraic notation
    """
    columncaptured=""
    columncapturedAlg=""
    
    listOfCaptures=[]
    listOfPossibleCaptures=[]
    columngrabber=""
    columngrabberAlg=""
    side=""
    ambiguitypiecesgrabber=False
    capture=move.split('x')

    grabbermove=capture[0]
    capturedmove=capture[1]
    
    grabberSpaPiece=grabbermove[0]
    capturedSpaPiece=capturedmove[0]

    # grabber in English notation
    grabber=Spa2EngPiece(grabberSpaPiece)
    # captured in English notation
    captured=Spa2EngPiece(capturedSpaPiece)

    print("grabber: " + grabber)
    print ("captured: " + captured)


    # There are 4 cases: 
    # 1 PxP (no columns specified, just pieces)
    # 2 PDxPR (both columns are spcified)
    # 3 PDxP (column grabber is
    #  specified)
    # 4 PxPD (column capturer is specified)

   

    # Case 2: grabber is 2 or 3 length => PDxP or PTRxP for example

    if (len(grabbermove)!=1): 
        columngrabber=grabbermove[1:] # we get string from column until end
        if (columngrabber=='R' or (columngrabber=='D')):
            print("column or side grabber:"  + columngrabber)
            side=columngrabber
            ambiguitypiecesgrabber=True
            print("AlgColumn grabber or side:" + columngrabber)
        else:            
          print("Ambigous grabber")
          print("Ambiguous column grabber")
          columngrabber=check_colambiguities(columngrabber)
          print(columngrabber)
          columngrabberAlg=convert_list_col_desc_alg(columngrabber)
          print(columngrabberAlg)

        

    print("White Turn: " + str(whiteT))
     # Case 3: captured is 2 or 3 length => PxDC or PxPTR

    if (len(capturedmove)==2 or (len(capturedmove)==3)):
        columncaptured=capturedmove[1:]
        if (columncaptured=='R' or (columncaptured=='D')):
            print("column captured or side captured: " + columncaptured)
            columncapturedAlg=Desc2AlgCol(columncaptured)
            print("No column captured ambiguity")
            print("AlgColumn captured: " + columncapturedAlg)
        else:
            print("Ambigous captured")
            print("Ambigous columns")
            columncaptured=check_colambiguities(columncaptured)  
            print(columncaptured) # print descriptive ambiguous column
            columncapturedAlg=convert_list_col_desc_alg(columncaptured)
            print(columncapturedAlg) # print algebraic ambigous column
         

    # Get all legal moves (in UCI format) we can do
    legalUCImoves=list(board.legal_moves)
    # We only get captures with grabbers on it
    for legalUciMove in legalUCImoves:
        # Convert UCi move notation to Algebraic notation
        movAlg=board.san(legalUciMove)
        if "x" in movAlg:            
            listOfPossibleCaptures.append(movAlg)
    print ("List Of possible captures: " + str(listOfPossibleCaptures))

    for movAlg in listOfPossibleCaptures:
            currentmove=movAlg.split('x') 
            # We separate current grabber & captured in legal capture
            currentgrabber=currentmove[0]
            currentcaptured=currentmove[1]
            if (grabber=="P"):
                # If it is a pawn we look for grabbers in lowercase
                if (currentgrabber.islower()):
                    # If colAlg is definied we only add that legal capture
                    if (columngrabberAlg!=""):
                        # if colAlg == current grabber (pawn) col it is a capture
                        if (columngrabberAlg==currentgrabber):
                            listOfCaptures.append(movAlg)
                    else:
                        listOfCaptures.append(movAlg)
            # we check grabber piece legal capture with grabber of move
            elif grabber in currentgrabber:
                               
                if(columncapturedAlg!=""):
                    for colAlg in columncapturedAlg:
                        if (colAlg==currentcaptured[0]):
                            listOfCaptures.append(movAlg)           
                else:
                    if (side=="D"):
                        if (movAlg[1]<='d'):
                            print("Legal move is " + movAlg)
                            board.push_san(movAlg)
                            return(movAlg)
                        elif(side=="R"):
                            if movAlg[1]>='e':
                                print("Legal move is " + movAlg)
                                board.push_san(movAlg)
                                return(movAlg)
                    listOfCaptures.append(movAlg)
                           
                    
    print("List of legal captures " + str(listOfCaptures) + "for grabber=>"  + str(grabber))
    numberOfCaptures=len(listOfCaptures)

    if(numberOfCaptures==1):

        movAlg=listOfCaptures[0]
        print(movAlg)
        board.push_san(movAlg)
        return(movAlg)
    else:
        movAlg=check_capture(grabber,captured,listOfCaptures,whiteT)
        board.push_san(movAlg)
        return(movAlg)
    
       
                        


# Funcion para traducir descriptive-algebraico
def converter(move,whiteT):
    ''' function to convert from descriptive to algebraic

    Parameters:
    move (string): move in descriptive notation
    whiteT (bool): bool to check if it is white turn
    '''
    ambiguity=False
    index=0
    length=len(move)
    columnmove=""
    indice=0
    side=""
    row=""
    ambiguitypieces=False
    
    # check kind of move
     
    # short or long castling
    if (move=="O-O")or(move=="O-O-O"):
        board.push_san(move)
        return move
    # it is a capture
    elif('x' in move) or ('X' in move):
       move=capture(move,whiteT)
       return move
    # it is checkmate
    elif(move=="++"):
    # it no move (last line and black no move)
        return move      
    # it is a move. Locate row first 
    else:
        for caracter in move:
            if caracter.isdigit():
                row=caracter
                break
            else:
                indice=indice+1
        
        piece=move[0:indice]
        col=move[indice+1:]
        print ("Pieza to move: " + piece)
        print("Row to move (white): " + row)
        print("Col to move: " + col)
        if piece in Spapieces:
            print("Just 1 piece can go to destiny")
        else:
            print ("Two pieces can go to destiny")
            print("Piece: " + piece[0] +" of side " + piece[1])
            side=piece[1]
            piece=piece[0]
            ambiguitypieces=True

       
        columnmove=check_colambiguities(col)
        if isinstance(columnmove,list):
            print("There's column ambiguity. Check both moves")
            print(columnmove)
            ambiguity=True
        else:
            ambiguity=False
  

    for Spapiece in Spapieces:
        if (Spapiece==piece):
            break
        index=index+1
    
   # Get the English name of the piece
    EnglishPiece=Spa2EngPiece(piece)
        # if it is white turn, row is ok in descriptive notation
    if (not whiteT):
        # if it is black turn, row in descriptive is 9-row    
        row=str(9-int(move[1]))


 #There's no ambiguity, we know right column
    if (not ambiguity):
        print("There's no ambiguity in cols")
        print("Column move: " + columnmove)

        col=Desc2AlgCol(columnmove)
    
        if (ambiguitypieces): # Two pieces can go same square: Nce4 Nge4
            legalUCImoves=list(board.legal_moves)
            for legalUciMove in legalUCImoves:
                movAlg=board.san(legalUciMove)
                if EnglishPiece in movAlg: # Look for pieces in movements
                    if col in movAlg:      # Look for pieces that go same col
                        if row in movAlg:  # Look for pieces that go same row
                            if (side=="D"): # Queen side => cols a-d
                                if movAlg[1]<='d':
                                    print("Legal move is " + movAlg)
                                    board.push_san(movAlg)
                                    return(movAlg)

                            elif (side=="R"): # King side => cols e-h
                                if movAlg[1]>='e':
                                    print("Legal move is " + movAlg)
                                    board.push_san(movAlg)
                                    return(movAlg)
    
      

    else:
        print("There is ambiguity")
        colA=Desc2AlgCol(columnmove[0]) # A option 
        colB=Desc2AlgCol(columnmove[1]) # B opcton 
        
        if (piece!="P"):
            print("A Option: " + piece+colA+row)
            print("B Option: " + piece+colB+row)
        else: 
            print("A Option: " + colA+row)
            print("B Option: " + colB+row)

        # Trying a illegal move give an exception. We catch it to get the right one.
        try:
            if (piece!="P"):
                board.push_san(EnglishPiece+colA+row)
            else:
                board.push_san(colA+row)
        except Exception:
            print("A Option is ilegal!")
            if (piece !="P"):
                print("Legal Move: " + piece+colB+row)
            else:
                print("Legal Move: " + colB+row)
            
            col=colB

        try:
            if (piece!="P"):
                board.push_san(EnglishPiece+colB+row)
            else:
                board.push_san(colB+row)
        except Exception:        
            print("B Option is illegal!")
            if(piece!="P"):
                print("Legal Move: " + piece+colA+row)
            else:
                print("Legal Move: " + colA+row)
            
            col=colA
        board.pop() #undo last move that we did to get the rigth one

    # We print the move we are going to do
    print(piece+col+row)
    
    if (piece=='P'): # If a pawn is moved piece name isn't included
        board.push_san(col+row)      
    else:
        board.push_san(EnglishPiece+col+row)

    if (piece != "P"):
        return(EnglishPiece+col+row)  
    else:
        return(col+row)


def create_pgn_file_head(archivoAlg):
    archivoAlg.write('[Event "?"]\n[Site "?"]\n[Site "?"]\n[Date "????.??.??"]\n[Round "?"]\n\
[White "?"]\n[Black "?"]\n[Result "?-?"]\n\n')


#[Event "?"]
#[Site "?"]
#[Date "????.??.??"]
#[Round "?"]
#[White "?"]
#[Black "?"]
#[Result "?-?"]


def absolutepath(dir):
    script_dir=os.path.dirname(__file__)
    # Relative paths to script path for origin and destination directories
    abs_dir_path=os.path.join(script_dir+dir)
    return(abs_dir_path)

def main():

    args=len(sys.argv)
    origfile=""
    destfile=""

    # Solo realizamos la conversión de un único fichero  que seleccionamos
    if (args==1):

        destdir="\\sample output files"
        origdir="\\sample input files"

        abs_dir_pathOrig=absolutepath(origdir)
        abs_dir_pathDest=absolutepath(destdir)
                    
        # Destination file (.pgn extension to be imported or pasted in chess software)
        #destfile=input("Output File Name (.pgn): ")
        origfile=tkinter.filedialog.askopenfile(initialdir=abs_dir_pathOrig,title="Select source file in spanish descriptive format")
        
        # Ask for input file via filedialog (Spanish descriptive chess notation file)
        # By default there is a folder called sample input files
        # For example, Damiano's gambit.txt file
        # 1. P4R P4R 
        # 2. C3AR P3AR
        # 3. CxP PxC
        # 4. D5T R2R
        # 5. DxPR R2A
        # 6. A4A R3C    
        # 7. D5AR R3T
        # 8. P4D P4CR
        # 9. P4TR A2R
        # 10. PxP R2C
        # 11. D7A ++


        destfile=tkinter.filedialog.asksaveasfile(initialdir=abs_dir_pathDest,defaultextension=".pgn",filetypes=(("PGN file","*.pgn"),),title="Write conversion in pgn file")
        
        # Ask for save file via filedialog
        # By default there will go to output directory
    else:
        print(sys.argv)
        # Argv 1 => absolute file path
        # Argv 2 => file name
        # Argv 3 => dest dir

        abspathorigfilename=sys.argv[1]
        destdir=sys.argv[3]
        filename=sys.argv[2]
        destname=filename.split(".")
        destfilename=destname[0]+".pgn"
        abspathdestfilename=join(destdir,destfilename)

        print("Destdir: " + destdir)
        print("destfilename: "  + destfilename)
        print("abspathdestfilename: " + abspathdestfilename)
        
        origfile=open(abspathorigfilename,'r')
        destfile=open(abspathdestfilename,'w')

       


    printDefaultBoard()

    # Open output file for writing
    with origfile:
        # pgn files must have a head of 7 lines
        create_pgn_file_head(destfile)

        # Open input file for reading
        with destfile:
            # Initializate moves
            nmove=1
            for move in origfile:
                if (move!="\n"):
                    print("move: " + str(nmove))
                    currentmove=move.split()
                    whitemove=currentmove[1]
                    if (len(currentmove)<3): # There's no black move in file
                        blackmove=""
                    else:
                        blackmove=currentmove[2]
                    print ("white move descriptive:  " + whitemove)
                    moveBAlg=converter(whitemove,True)
                    print ("white move algebraic: " +moveBAlg)
                    print(board)
                    print("--------")
                    if (blackmove!=""):
                        print ("black move descriptive: " + blackmove)
                        moveNAlg=converter(blackmove,False)
                        print ("black move descriptive: " + moveNAlg)
                        print(board)
                        print("========")
                    else: # There's no black move=>empty move
                        moveNAlg=blackmove
                    # Print to the pgn file
                    destfile.write(str(nmove) + ". " + moveBAlg + " " + moveNAlg +"\n")

                    nmove=nmove+1

    # Closing files
    origfile.close()
    destfile.close()

if __name__=="__main__":    
    main()