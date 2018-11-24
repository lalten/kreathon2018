import { Component, OnInit, OnChanges, SimpleChanges, ViewChild, ElementRef, Input } from '@angular/core';
import { ContainerService } from '../../service/container/container.service';
import { Container } from '../../model/container';
import {Coordinate} from '../../model/coordinate';
import {Marker} from '../../model/marker';
import { Subscription, timer, pipe } from 'rxjs';
import { switchMap } from 'rxjs/operators';


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
    private container : Container[] = [];
    private route_marker = [];
    private directions = [];
    private group;
    private is_route : boolean = false;
    private instructions = [];
    private abholen = [];


    //config for here
    appId: any = "nAX0YLEqe9rDAffuvS9L";
    appCode: any = "O_9Z4uw6cbqaUNKCrWvAlg";

    //These are the coordinates of Krefeld
    lat: any = "51.33276";
    lng: any = "6.58217";

    //This is for inteveral (automatic reload)
    subscription: Subscription;


    //constructor
    public constructor(private containerService : ContainerService) {
        var that = this;

        this.platform = new H.service.Platform({
            "app_id": "nAX0YLEqe9rDAffuvS9L",
            "app_code": "O_9Z4uw6cbqaUNKCrWvAlg"
        });
    }

    //onInit
    public ngOnInit() { 
       //create here platfrom
       this.platform = new H.service.Platform({
        "app_id": this.appId,
        "app_code": this.appCode
      });

      this.router = this.platform.getRoutingService();
    }

    //After init
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
      

      this.subscription = timer(0, 5000).pipe(
        switchMap(() => this.containerService.getContainer())
      ).subscribe(result => this.parseContainer(this, result));
      

    }

    //parse container dat
    private parseContainer(context, container) {
        if(this.is_route){
          return;
        }  

        context.clearContainer();

        for(var i = 0; i < container['containers'].length; i++){
          var item = container['containers'][i];
          if(item.id == 1){
            console.log(item['level']);
          }
          
          let c : Container = new Container(item.id, item.clean, item['level'], new Coordinate(item['lat'], item['lng']), item['loc_str']);
          context.container.push(c)
        }


        context.renderContainer();
    }

    //delete container data
    private clearContainer(){
      if(this.is_route == true){
        return;
      }

      if(this.container.length > 0){
        for(var i = 0; i < this.container.length; i++){
          this.map.removeObject(this.container[i]['obj_marker']);
        }
      }

      this.container = [];
    }

    //render container data
    private renderContainer(){
      var that = this;

      this.container.forEach(function(container){
        that.addMarkerForContainer(container);
      });
    }

    //Add a marker for a container
    private addMarkerForContainer(container : Container){
      var that = this;

      var url;
      if(container.full > 95){
        url = "./assets/marker_full.png"
      }
      else if(container.full > 80){
        url = "./assets/marker_80.png"
      }
      else if(container.full > 60){
        url = "./assets/marker_60.png"
      }
      else if(container.full > 40){
        url = "./assets/marker_40.png"
      }
      else if(container.full >20){
        url = "./assets/marker_20.png"
      }
      else {
        url = "./assets/marker_empty.png"
      }

      //create icon
      var icon = new H.map.Icon(url, {size: {w: 32, h: 32}});

      let m = new H.map.Marker({'lat' : container.coordinates.lat, 'lng' : container.coordinates.ltd}, {icon : icon});

      //set marker data
      this.setMarkerData(m, container);

      m.addEventListener('tap', function (evt) {
        var bubble =  new H.ui.InfoBubble(evt.target.getPosition(), {
          // read custom data
          content: evt.target.getData()
        });
        // show info bubble
        that.ui.addBubble(bubble);
        bubble.open();
        
      }, false);

      container['obj_marker'] = m;

      //add to map
      this.map.addObject(m);
     
    }

    //Add Bubble popup 
    private setMarkerData(marker, container){
      var html = "<div class='bubble'><h3>" + container.street + "</h3><dl><dt>ID:</dt><dd>" + container.id + "</dd><dt>Voll:</dt><dd>" + container.full + "%</dd><dt>Sauber:</dt><dd>" + container.clean + "</dd></dl></div>";
      marker.setData(html);
    }

    //Add this marker
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

    //Add route highlight
    private addRouteHighlightMarker(lat, lng){
      let icon = new H.map.Icon("https://cdn0.iconfinder.com/data/icons/small-n-flat/24/678111-map-marker-512.png", {size: {w: 32, h: 32}});
      let m = new H.map.Marker({'lat' : lat, 'lng' : lng}, {icon : icon});

      //add to map
      this.map.addObject(m);

      this.route_marker.push(m);
    }

    //set a marker as dragable
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

    //Start for a route
    private addRouteStart(){
      this.addMarkerForRoute();
    }

    //calculate the route for a given cocntainer
    private calculateRoute(params, container){
      var that = this;

      //Clear and redraw
      for(var i = 0; i < this.container.length; i++){
        //First remove
        try {
          this.map.removeObject(this.container[i]['obj_marker']);
        }
        catch(e){
          console.log(e);
        }
        
        //Then add new one
        this.addMarkerForContainer(this.container[i]);
      }

      return new Promise((resolve, reject) => {
          //Calculate route
          that.router.calculateRoute(params, data => {
            if(data.response){
                var length = 0;
                let dirs = [];
                let instructions = [];

                for(var i = 0; i < data.response.route[0].leg.length; i++){
                  let directions = data.response.route[0].leg[i].maneuver;
                  
                  dirs += directions;

                  for(var j = 0; j < directions.length; j++){
                    length += directions[j].length;
                    instructions.push(directions[j].instruction)
                  }
                }
                
                resolve({directions : dirs , length : length, data : data.response.route[0], container : container, instructions : instructions});
            }

            
          }, error => {
            console.error(error);
            return {directions : {}, length : -1, data : null}
        });
      });
    }

    //wrapper function for adding params
    private calculateRouteWithContainer(container : Container){
       //Basic params
       var params = {
        'waypoint0' : 'geo!' + this.route_marker[0].getPosition().lat + ',' + this.route_marker[0].getPosition().lng,
        'waypoint1' : 'geo!' + container.coordinates.lat + ',' + container.coordinates.ltd,
        'waypoint2' : 'geo!' + this.route_marker[1].getPosition().lat + ',' + this.route_marker[1].getPosition().lng,
        'mode': 'shortest;car',
        'representation': 'display'
      };

      return this.calculateRoute(params, container);
     
    }

    //get minimum route
    private getMinRoute(){
      var that = this;

      return new Promise((resolve, reject) => {
        let min = 1000000;
        let best = {};
        let edited = [];
        let best_container = {};

        that.container.forEach(function(container){
            if(container.full < 95){

            that.calculateRouteWithContainer(container).then(function(result){
              edited.push(result);

              if(result['length'] > 0 && result['length'] < min){
                
                min = result['length'];
                best = result;
              }

              if(edited.length > (that.container.length - 10)){
                resolve(best);
              }
            });
          }
          else {
            edited.push({})
          }
        });
      });
      
    }

    //display a route on map
    private displayRoute(length, directions, data, container, instructions){
      this.map.removeObject(container['obj_marker']);
      this.addRouteHighlightMarker(container.coordinates.lat, container.coordinates.ltd);

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

      this.instructions = instructions;
    }

    //start for route calculation
    private calculateMyRoute(){
      var that = this;


      if(this.route_marker.length < 2){
        alert("No start or destination");
        return;
      }

      this.is_route = true;
      

      this.getMinRoute().then(function(route){
        that.displayRoute(route['length'], route['directions'], route['data'], route['container'], route['instructions']);
      });
    }

    //get the best route
    private calculateBestRoute(){
      this.container.forEach(function(container){
        if(container.full > 95){
          this.abholen.push(container);
        }
      });
    }

    //show the round trip
    private  display_round_trip(container){
      var params = {
        //be fast
        'mode': 'shortest;car',
        'representation': 'display'
      };
      
      container.forEach(function(c, idx){
        params['waypoint' + idx] = 'geo!' + c.lat + ',' + c.lng;
      });

      this.router.calculateRoute(params, data => {
        if(data.response){
          let lineString = new H.geo.LineString();
          data = data.response.route[0];
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

        
      }, error => {
        console.error(error);
        return {directions : {}, length : -1, data : null}
    });

  }

  //listener for the round trip
  private roundTrip(){
    var that = this;
    this.containerService.getRoundRouteData().subscribe(function(data){
      that.display_round_trip(data);
    });
  }
}

