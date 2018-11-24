import {Coordinate} from './coordinate';
import {Marker} from './marker';

export class Container {
    id : number;
    clean : number;
    full : number;
    coordinates : Coordinate;
    street : string;
    marker : Marker;

    public constructor(id : number, clean : number, full : number, coordinate : Coordinate, street : string){
        this.id = id;
        this.clean = clean;
        this.full = parseInt(full.toFixed(2));
        this.coordinates = coordinate;
        this.street = street;
        //this.full = (100 * Math.random()); //Testing purposes
    }
}