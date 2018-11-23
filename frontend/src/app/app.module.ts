import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppComponent } from './app.component';
import { HereComponent } from './component/here/here.component';
import { RouterModule, Routes } from '@angular/router';
import { HttpClientModule, HttpClient } from '@angular/common/http';
import {HttpErrorHandlerService} from './service/http/http-error-handler.service';



const appRoutes: Routes = [
  { path: 'here', component: HereComponent }
];


@NgModule({
  declarations: [
    AppComponent,
    HereComponent
  ],
  imports: [
    BrowserModule,
    RouterModule.forRoot(
      appRoutes,
      { enableTracing: true } // debug
    ),
    HttpClientModule
  ],
  bootstrap: [AppComponent],
  providers: [HttpErrorHandlerService]
})  
export class AppModule { }
