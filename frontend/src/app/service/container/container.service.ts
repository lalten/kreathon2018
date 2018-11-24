
import { HttpErrorHandlerService, HandleError } from '../http/http-error-handler.service';
import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import {map, catchError} from "rxjs/operators";

import { Observable, throwError } from 'rxjs';
import { of } from 'rxjs';

import {Container} from '../../model/container';

import {Coordinate} from '../../model/coordinate';

@Injectable({
  providedIn: 'root'
})
export class ContainerService {

  private test_data : Container[] = [  
      new Container(1, 0, 0, new Coordinate(51.33608,6.63602), 'asd'),
      new Container(2, 0, 0, new Coordinate(51.348621,6.64751), 'asd'),
      new Container(3, 0, 0, new Coordinate(50.221108,8.621942), 'asd'),
      new Container(4, 0, 0, new Coordinate(51.36249,6.62339), 'asd'),
      new Container(5, 0, 0, new Coordinate(51.36316,6.59766), 'asd'),
      new Container(8, 0, 0, new Coordinate(51.3358,6.64371), 'asd'),
      new Container(9, 0, 0, new Coordinate(51.330259,6.545865), 'asd'),
      new Container(10, 0, 0, new Coordinate(51.3165,6.57619), 'asd'),
      new Container(12, 0, 0, new Coordinate(51.339211,6.55931), 'asd'),
      new Container(15, 0, 0, new Coordinate(51.34465,6.54805), 'asd'),
      new Container(17, 0, 0, new Coordinate(51.339626,6.617302), 'asd'),
      new Container(18, 0, 0, new Coordinate(51.32936,6.62697), 'asd'),
      new Container(19, 0, 0, new Coordinate(51.31898,6.62664), 'asd'),
      new Container(21, 0, 0, new Coordinate(51.316460,6.602660), 'asd'),
      new Container(23, 0, 0, new Coordinate(51.319230,6.588010), 'asd'),
      new Container(25, 0, 0, new Coordinate(51.322891,6.580700), 'asd'),
      new Container(26, 0, 0, new Coordinate(51.316500,6.576190), 'asd'),
      new Container(28, 0, 0, new Coordinate(51.312031,6.558730), 'asd'),
      new Container(29, 0, 0, new Coordinate(51.308300,6.565790), 'asd'),
      new Container(30, 0, 0, new Coordinate(51.308690,6.589100), 'asd'),
      new Container(31, 0, 0, new Coordinate(51.305210,6.583580), 'asd'),
      new Container(33, 0, 0, new Coordinate(51.303040,6.580220), 'asd'),
      new Container(34, 0, 0, new Coordinate(51.294910,6.586550), 'asd'),
      new Container(35, 0, 0, new Coordinate(51.316479,6.589900), 'asd'),
      new Container(36, 0, 0, new Coordinate(51.331768,6.578997), 'asd'),
      new Container(38, 0, 0, new Coordinate(51.345242,6.590920), 'asd'),
      new Container(39, 0, 0, new Coordinate(51.343110,6.568970), 'asd'),
      new Container(40, 0, 0, new Coordinate(51.334660,6.563870), 'asd'),
      new Container(43, 0, 0, new Coordinate(51.330220,6.565961), 'asd'),
      new Container(44, 0, 0, new Coordinate(51.318310,6.561890), 'asd'),
      new Container(45, 0, 0, new Coordinate(51.333940,6.600560), 'asd'),
      new Container(46, 0, 0, new Coordinate(51.336491,6.570110), 'asd'),
      new Container(48, 0, 0, new Coordinate(51.335980,6.556940), 'asd'),
      new Container(50, 0, 0, new Coordinate(51.334492,6.565060), 'asd'),
      new Container(51, 0, 0, new Coordinate(51.320970,6.546540), 'asd'),
      new Container(52, 0, 0, new Coordinate(51.321080,6.527850), 'asd'),
      new Container(53, 0, 0, new Coordinate(51.329960,6.536940), 'asd'),
      new Container(54, 0, 0, new Coordinate(51.344067,6.552482), 'asd'),
      new Container(55, 0, 0, new Coordinate(51.349869,6.552332), 'asd'),
      new Container(56, 0, 0, new Coordinate(51.346430,6.545919), 'asd'),
      new Container(57, 0, 0, new Coordinate(51.452205,6.638454), 'asd'),
      new Container(64, 0, 0, new Coordinate(51.351270,6.650410), 'asd'),
      new Container(65, 0, 0, new Coordinate(51.333450,6.572000), 'asd'),
      new Container(66, 0, 0, new Coordinate(51.325859,6.557780), 'asd'),
      new Container(67, 0, 0, new Coordinate(51.338820,6.574970), 'asd'),
      new Container(69, 0, 0, new Coordinate(51.363541,6.614750), 'asd'),
      new Container(71, 0, 0, new Coordinate(51.320389,6.563060), 'asd'),
      new Container(73, 0, 0, new Coordinate(51.329617,6.670257), 'asd'),
      new Container(75, 0, 0, new Coordinate(51.331713,6.679759), 'asd'),
      new Container(76, 0, 0, new Coordinate(51.337009,6.660000), 'asd'),
      new Container(77, 0, 0, new Coordinate(51.344158,6.641220), 'asd'),
      new Container(78, 0, 0, new Coordinate(51.358160,6.646050), 'asd'),
      new Container(79, 0, 0, new Coordinate(51.362070,6.573890), 'asd'),
      new Container(80, 0, 0, new Coordinate(51.336460,6.547930), 'asd'),
      new Container(82, 0, 0, new Coordinate(51.340721,6.537810), 'asd'),
      new Container(83, 0, 0, new Coordinate(51.334301,6.546460), 'asd'),
      new Container(84, 0, 0, new Coordinate(51.348358,6.527010), 'asd'),
      new Container(85, 0, 0, new Coordinate(51.347480,6.520020), 'asd'),
      new Container(86, 0, 0, new Coordinate(51.363708,6.521440), 'asd'),
      new Container(88, 0, 0, new Coordinate(51.370293,6.497376), 'asd'),
      new Container(90, 0, 0, new Coordinate(51.371940,6.497830), 'asd'),
      new Container(91, 0, 0, new Coordinate(51.320091,6.552320), 'asd'),
      new Container(96, 0, 0, new Coordinate(51.341310,6.599210), 'asd')
  ]; 

  

  private genrateTestData() : Container[]{
    let result : Container[] = [];

    

    for(var i = 0; i < 60; i++){
      let lat = 51.31 + ((1/(Math.random() % 1000000000))); 
      let lng = 6.50 + ((1/(Math.random() % 1000000000))); 
      let c : Container = new Container(i, 1, 1, new Coordinate(lat, lng), 'asf');
      result.push(c);
    }

    return result;
  }
  constructor(private http: HttpClient, httpErrorHandler: HttpErrorHandlerService) {
    this.handleError = httpErrorHandler.createHandleError('ContainerService');
  }

  //handlers
  private handleError: HandleError;
  

  private responseToContainer(response) : Container[] {
    let result : Container[] = [];

    response.forEach(function(item){
      let c : Container = new Container(item.id, item.clean, item.level, new Coordinate(item.lat, item.lng), item.loc_tr);
      result.push(c)
    });

    return result;

  }

  public getContainer() : Observable<Container[]> {
    return this.http.get<Container[]>('/containers');

   
   /* .map((response : any[]) => {
      let result : Container[] = [];

      response.forEach(function(item){
        let c : Container = new Container(item.id, item.clean, item.level, new Coordinate(item.lat, item.lng), item.loc_tr);
        result.push(c)
      });

      return result;
    })
    .pipe(                                                                            
      catchError(this.handleError('load_container', []))
    ); */
     

  }
  
  public getRoundRouteData() : Observable<Container[]> {
    return of(this.test_data);
  }
  
}
