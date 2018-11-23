import { Coordinate } from "./coordinate";


export class Marker {
    here_marker : any;
    coordinates : Coordinate;
    type : number; //normal, position, hof

    public constructor(here_marker : any, coordinates : Coordinate, type : number){
        this.here_marker = here_marker;
        this.coordinates = coordinates;
        this.type = type;
    }
}