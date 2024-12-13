# TODO:

* database models
    
    * tanks (players)
    
    * bullets

    * games

* check for collisions in the backend

* basically everything from the frontend

# JSONs:

Each player will send their state to the server and the server will broadcast relevant data for each player to render the game. Will struct the data on event-type jsons:

## event: state

### Client to server:

~~~ py
{
    event: "state",
    data: {
        name: string,
        mousex: int,
        mousey: int,
        tankx: int,
        tanky: int,
        shooting: bool 
    }
}
~~~

### Server to client:

~~~ py
{
    event: "state",
    data: {
        name: string,
        tankx: int,
        tanky: int,
        angle: float,
        health: int,
    }
}
~~~

## Event add_tank:

### Client to server:

~~~ py
{
    event: "add_tank",
    data: {
        name: string
    } 
}
~~~

### Server to client

~~~ py
{
    event: "init_tank"
    data: {
        name: string,
        tankx: int,
        tanky: int,
        angle: float,
        health: int,
    }
}