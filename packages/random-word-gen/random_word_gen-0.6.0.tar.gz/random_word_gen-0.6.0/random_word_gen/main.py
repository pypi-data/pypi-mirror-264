import random
list_of_words = ['adventure', 'animal', 'answer', 'apple', 'area', 'asleep', 'auspicious', 'awake',
                'aware', 'ball', 'banana', 'beans', 'bed', 'begin', 'beginning', 'best', 'big', 
                'billion', 'body', 'bomb', 'bracket', 'breadth', 'camera', 'campus', 'case', 'chicken', 
                'circumference', 'coding', 'collage', 'college', 'confetti', 'diameter', 'differentiate', 
                'diffusion', 'discomfort', 'dispenser', 'dispersion', 'distant', 'dragon', 'ear', 
                'easter', 'egg', 'eigth', 'escape', 'everywhere', 'eye', 'face', 'fifth', 'fire', 'first', 
                'fish', 'fourth', 'fox', 'fruits', 'gamer', 'gaming', 'giant', 'graph', 'happening', 
                'happy', 'heavenly', 'height', 'hello', 'here', 'honesty','honestly', 'hundred', 'input', 'integration', 
                'intelligence', 'intimacy', 'intimidate', 'is', 'laptop', 'length', 'lightning', 'lights', 
                'list', 'luscious', 'machine', 'mathematics', 'mattress', 'million', 'mobile', 'movie', 
                'ninth', 'nose', 'olive', 'one', 'output', 'perimeter', 'phone', 'pizza', 'policy', 
                'positive', 'psychotic', 'quickly', 'real', 'reflect', 'reflecting', 'reflection', 
                'refraction', 'repercussions', 'sad', 'sausage', 'science', 'second', 'sensual', 'seventh', 
                'sixth', 'sleeping', 'sly', 'small', 'snowflake', 'song', 'songwriter', 'stew', 'string', 
                'surely', 'tenth', 'the', 'there', 'third', 'thousand', 'timer', 'tired', 'train', 'trillion', 
                'uncomfortable', 'understand', 'understanding', 'understatement', 'university', 'unreal', 
                'volume', 'was', 'water', 'website', 'where', 'width', 'word', 'words',
                'special','secret','secretive','radius','registration','keyboard','mouse','rat','sea',
                'bird','speaker','door','table','fork','knife','spoon','key','apartment','compartment',
                'department','meant','solution','find','statue','student','administrator',
                'laboratory','account',
                ]

list_of_colours = ['red','wine red','blood red','crimson','scarlet'
                   'yellow',
                   'blue','sky blue','aqua','cyan','teal','royal blue','turquoise',
                   'green','olive green','mint green','lime green',
                   'pink','magenta','fuschia','hot pink',
                   'purple','lilac','lavendar','amethyst',
                   'white',
                   'black','dark grey',
                   'brown','hazelnut brown','chocolate',
                   'orange',
                   'grey', 'ash grey','light grey',
                   'silver',
                   'gold','rose gold',
                   'peach','tan'
                   ]

def random_word():
    rand = random.randrange(0,len(list_of_words)+1)
    return list_of_words[rand]

def random_colour():
    rand = random.randrange(0,len(list_of_colours)+1)
    return list_of_colours[rand]