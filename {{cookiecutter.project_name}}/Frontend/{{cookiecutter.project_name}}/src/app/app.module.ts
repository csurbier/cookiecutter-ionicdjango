import { NgModule, ErrorHandler, Injectable } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { RouteReuseStrategy } from '@angular/router';

import { IonicModule, IonicRouteStrategy ,Platform} from '@ionic/angular';
import { SplashScreen } from '@ionic-native/splash-screen/ngx';
import { StatusBar } from '@ionic-native/status-bar/ngx';

import { AppComponent } from './app.component';
import { AppRoutingModule } from './app-routing.module';
import { HttpBackend, HttpXhrBackend, HttpInterceptor, HttpEvent, HttpRequest, HttpHandler, HttpErrorResponse } from '@angular/common/http';

import { HttpClientModule, HttpClient } from '@angular/common/http';
import { HTTP_INTERCEPTORS} from '@angular/common/http';
import { HTTP } from '@ionic-native/http/ngx';
import { Observable } from 'rxjs';
import { timeout } from 'rxjs/operators';
import { NativeHttpModule, NativeHttpBackend, NativeHttpFallback } from 'ionic-native-http-connection-backend';


@Injectable()
export class AngularInterceptor implements HttpInterceptor {
  intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    let defaultTimeout = 10000;
      return next.handle(req).pipe(timeout(defaultTimeout));
    
    // 10000 (10s) would be the global default for example
  }
}
class MyErrorHandler implements ErrorHandler {
  handleError(error: Error | HttpErrorResponse) {
    // do something with the exception
    if (error instanceof HttpErrorResponse) {
      // Server or connection error happened
      console.log("=====>MyErrorHandler: statusCode: "+error.status)
   } else {
     // Handle Client Error (Angular Error, ReferenceError...)  
     console.log("=====>MyErrorHandler:")
     console.log(error)   
   }
   
  }
}

@NgModule({
  declarations: [AppComponent],
  entryComponents: [],
  imports: [
    BrowserModule, 
    IonicModule.forRoot(), 
    NativeHttpModule,
    AppRoutingModule,
    HttpClientModule,
  ],
  providers: [
    StatusBar,
    SplashScreen,
    HTTP,
    {provide: HttpBackend, useClass: NativeHttpFallback, deps: [Platform, NativeHttpBackend, HttpXhrBackend]},
    { provide: RouteReuseStrategy, useClass: IonicRouteStrategy },
    { provide: HTTP_INTERCEPTORS, useClass: AngularInterceptor, multi: true } ,
  ],
  bootstrap: [AppComponent]
})
export class AppModule {}