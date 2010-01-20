"""
seqparse contains definitions of parsers that are used to
extract sequence information from files. These parsers
feed the data to their respective dict writers which
create the databases
"""
import fqByIntDict
import fqByKeyDict
import faByIntDict
import faByKeyDict
import dbEntries

class DbException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

def read_fastq_sequences(filename, dbType='index'):
    """
    Function to parse text from the given FASTQ file into a sqeaqr database.
    dbType specifies if the database will use integer or text keys 
    """

    # [AN] when write other version of fqDict, put in check for 'int' vs 'key' or something

    try:
        theFile = open(filename, "rb")
    except IOError, e: 
        raise DbException(str(e))

    fqDb = None
    if dbType == 'index':
        fqDb = fqByIntDict.sqeaqrDB(filename)
    elif dbType == 'key':
        fqDb = fqByKeyDict.sqeaqrDB(filename)
    else:
        print "Invalid dbType specified: %s" % dbType
        exit(1)

    while 1:
        # [AN] does this have to be empty? could make set here instead of in db
        data = [0] # Emtpy index entry 
        firstLine = theFile.readline().strip().split('@')
        if len(firstLine) == 1: # Reached eof
            break
        # Make sure the FASTQ file is being read correctly
        assert firstLine[0] == ''
        name = firstLine[1]
        data.append(name) # The name
        data.append(theFile.readline().strip()) # The sequence
        theFile.read(2) # Ignore the '+\n'
        data.append(theFile.readline().strip()) # The accuracy
        fqDb[name] = dbEntries._sqeaqr_record(zip(dbEntries.FASTQFIELDS, data))

    theFile.close()
    fqDb.close()

def read_fasta_sequences(filename, dbType='index'):
    """
    Function to parse text from the given FASTA file into a sqeaqr database.
    dbType specifies if the database will use index or text keys
    """
    try:
        theFile = open(filename, "rb")
    except IOError, e:
        raise DbException(str(e))

    # [AN] when write other version of fqDict, put in check for 'int' vs 'key' or something
    faDb = None
    if dbType == 'index':
        faDb = faByIntDict.sqeaqrDB(filename)
    elif dbType == 'key':
        faDb = faByKeyDict.sqeaqrDB(filename)
    else:
        print "Invalid dbType specified: %s" % dbType
        exit(1)

    # Parse text and add to database
    nextChar = theFile.read(1)
    while nextChar != '':
        data = [0] # Empty index entry
        assert nextChar == '>'
        topLine = theFile.readline().strip().split(' ', 1)

        # Extract the name
        name = topLine[0]
        data.append(name) # The name

        # Extract the description
        description = ''
        if len(topLine) == 2:
            description = topLine[1]
        data.append(description) # The description

        # Collect sequence lines into a list
        sequenceList = []
        nextChar = theFile.read(1)
        while nextChar != '' and nextChar != '>':
            sequenceLine = nextChar + theFile.readline().strip()
            sequenceList.append(sequenceLine)
            nextChar = theFile.read(1)
            
        sequence = "".join(sequenceList)
        data.append(sequence) # The sequence
        faDb[name] = dbEntries._sqeaqr_record(zip(dbEntries.FASTAFIELDS, data))
            
    theFile.close()
    faDb.close()

# # Parser for the fake 'hava' sequence
## def read_hava_sequences(filename, multiplier=2):
##     """
##     Function to parse text from the given HAVA file into a screed database
##     """
##     try:
##         theFile = open(filename, "rb")
##     except IOError, e:
##         raise dbw.DbException(str(e))

##     attributes = ("hava", "quarzk", "muchalo", "fakours", "selimizicka", "marshoon")
##     db = openDBW(attributes, filename, multiplier)

##     if db.is_open() == False:
##         raise dbw.DbException("ERROR: DATABASE FILES ARE NOT OPEN")

##     # Parse text and add to database
##     nextChar = theFile.read(1)
##     while nextChar != '':
##         hava = nextChar + theFile.readline().strip()
##         quarzk = theFile.readline().strip()
##         muchalo = theFile.readline().strip()
##         fakours = theFile.readline().strip()
##         selimizicka = theFile.readline().strip()
##         marshoon = theFile.readline().strip()

##         recordString, attributeLengths = combineRecord((hava, quarzk, muchalo,
##                                                         fakours, selimizicka,
##                                                         marshoon))
##         db.writeRecord(recordString, attributeLengths)
##         nextChar = theFile.read(1)

##     theFile.close()
##     db.close()
