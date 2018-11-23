import { Component, OnInit, OnChanges, SimpleChanges, ViewChild, ElementRef, Input } from '@angular/core';
import { ContainerService } from '../../service/container/container.service';
import { Container } from '../../model/container';
import {Coordinate} from '../../model/coordinate';
import {Marker} from '../../model/marker';

declare var H: any;

@Component({
  selector: 'app-here',
  templateUrl: './here.component.html',
  styleUrls: ['./here.component.css']
})
export class HereComponent implements OnInit {

    @ViewChild("map")
    public mapElement: ElementRef;

    //private attributes
    private platform: any;
    private behavior : any;
    private map : any;
    private ui : any;
    private router: any;

    //private class data
    private container : Container[];
    private route_marker = [];
    private directions = [];
    private group;


    //config
    appId: any = "nAX0YLEqe9rDAffuvS9L";
    appCode: any = "O_9Z4uw6cbqaUNKCrWvAlg";

    //These are the coordinates of Krefeld
    lat: any = "51.33276";
    lng: any = "6.58217";

  

    public constructor(private containerService : ContainerService) {
        var that = this;

        this.platform = new H.service.Platform({
            "app_id": "nAX0YLEqe9rDAffuvS9L",
            "app_code": "O_9Z4uw6cbqaUNKCrWvAlg"
        });

        
    }

    public ngOnInit() { 
       //create here platfrom
       this.platform = new H.service.Platform({
        "app_id": this.appId,
        "app_code": this.appCode
      });

      this.router = this.platform.getRoutingService();
    }

    public ngAfterViewInit() {
      var that = this; //js stuff :D

      //set default layers
      let defaultLayers = this.platform.createDefaultLayers();   

      //init our map
      this.map = new H.Map(
          this.mapElement.nativeElement,
          defaultLayers.normal.map,
          {
              zoom: 13,
              center: { 
                lat: this.lat, 
                lng: this.lng 
              }
          }
      );

      //set behavior for interacitve map
      this.behavior = new H.mapevents.Behavior(new H.mapevents.MapEvents(this.map));
      this.ui = H.ui.UI.createDefault(this.map, defaultLayers, 'en-US');
      
     //load container
      this.containerService.getContainer().subscribe(function(container){
        that.container = container;
        that.renderContainer();
      });
    }

    private renderContainer(){
      var that = this;

      this.container.forEach(function(container){
        that.addMarkerForContainer(container);
      });
    }

    private addMarkerForContainer(container : Container){
      let m = new H.map.Marker({'lat' : container.coordinates.lat, 'lng' : container.coordinates.ltd});

      //add to map
      this.map.addObject(m);
    }

    private addMarkerForRoute(){
      if(this.route_marker.length >= 2){
        return;
      }

      let route_icon = new H.map.Icon("https://cdn1.iconfinder.com/data/icons/free-98-icons/32/map-marker-512.png", {size: {w: 32, h: 32}});

      let m = new H.map.Marker({'lat' : this.lat, 'lng' : this.lng}, {icon : route_icon}); //Add marker to middle

      //add to map
      this.map.addObject(m);

      //Make this dragable
      this.makeMarkerDragable(m);

      //add to route
      this.route_marker.push(m);
    }


    private makeMarkerDragable(marker){
      var that = this;
      
      //set marker as dragable
      marker.draggable = true;


      //disable map drag
      this.map.addEventListener('dragstart', function(ev) {
        var target = ev.target;
        if (target instanceof H.map.Marker) {
          that.behavior.disable();
        }
      }, false);

      //enable map listener on end
      this.map.addEventListener('dragend', function(ev) {
        var target = ev.target;
        if (target instanceof H.map.Marker) {
          that.behavior.enable();
        }
      }, false);

      this.map.addEventListener('drag', function(ev) {
        var target = ev.target,
            pointer = ev.currentPointer;
        if (target instanceof H.map.Marker) {
          target.setPosition(that.map.screenToGeo(pointer.viewportX, pointer.viewportY));
        }
      }, false);
    }

    private addRouteStart(){
      //this.addDragableMarker(new Coordinate(this.lat, this.lng));
      this.addMarkerForRoute();
    }

    private calculateRoute(params){
      var that = this;

      return new Promise((resolve, reject) => {
          //Calculate route
          that.router.calculateRoute(params, data => {
            if(data.response){
                var length = 0;
                let dirs = [];

                for(var i = 0; i < data.response.route[0].leg.length; i++){
                  let directions = data.response.route[0].leg[i].maneuver;
                  dirs += directions;

                  for(var j = 0; j < directions.length; j++){
                    length += directions[j].length;
                  }
                }
                
                resolve({directions : dirs , length : length, data : data.response.route[0]});
            }

            
          }, error => {
            console.error(error);
            return {directions : {}, length : -1, data : null}
        });
      });
    }

    private calculateRouteWithContainer(container : Container){
       //Basic params
       var params = {
        //be fast
        'waypoint0' : 'geo!' + this.route_marker[0].getPosition().lat + ',' + this.route_marker[0].getPosition().lng,
        'waypoint1' : 'geo!' + container.coordinates.lat + ',' + container.coordinates.ltd,
        'waypoint2' : 'geo!' + this.route_marker[1].getPosition().lat + ',' + this.route_marker[1].getPosition().lng,
        'mode': 'shortest;car',
        'representation': 'display'
      };

      return this.calculateRoute(params);
     
    }

    private getMinRoute(){
      var that = this;
     
      
      return new Promise((resolve, reject) => {
        let min = 1000000;
        let best = {};
        let edited = [];


        this.container.forEach(function(container){
            that.calculateRouteWithContainer(container).then(function(result){
              edited.push(result);

              console.log(result['length']);
              if(result['length'] > 0 && result['length'] < min){
                
                min = result['length'];
                best = result;
                console.log("Min setted: " + min);
              }

              if(edited.length == that.container.length){
                console.log(min);
                resolve(best);
              }
            });
        });

       
      });
      
    }

    private displayRoute(length, directions, data){
      let lineString = new H.geo.LineString();
      data.shape.forEach(point => {
          let parts = point.split(",");
          lineString.pushLatLngAlt(parts[0], parts[1]);
      });

      let lines = new H.map.Polyline(lineString, {
          style: { strokeColor: "blue", lineWidth: 5 }
      });

      if(!this.group){
        this.group = new H.map.Group();
        this.map.addObject(this.group);
      }
      else{
        this.group.removeAll();
      }
      
      //Add
      this.group.addObjects([lines]);
      this.map.setViewBounds(this.group.getBounds());
    }

    private calculateMyRoute(){
      var that = this;

      if(this.route_marker.length < 2){
        alert("No start or destination");
        return;
      }

      this.getMinRoute().then(function(route){
        that.displayRoute(route['length'], route['directions'], route['data']);
      });
    }



}

