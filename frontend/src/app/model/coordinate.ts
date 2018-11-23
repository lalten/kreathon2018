import { Marker } from "./marker";

export class Coordinate {
    lat : number;
    ltd : number;
    private marker : Marker;

    public constructor(lat : number, ltd : number){
        this.lat = lat;
        this.ltd = ltd;
    }
}