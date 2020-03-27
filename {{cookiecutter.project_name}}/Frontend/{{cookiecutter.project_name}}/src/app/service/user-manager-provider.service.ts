import { Injectable } from '@angular/core';
import { Observable, BehaviorSubject } from 'rxjs';
import { ApiserviceService } from './apiservice.service'
import { AppUser } from '../models/entities.ts';
import { Plugins } from '@capacitor/core';
import * as moment from 'moment';
import { UtilsProviderService } from './utils-provider';

const { Storage } = Plugins;
@Injectable({
  providedIn: 'root'
})
export class UserManagerProviderService {


  userLangue = "fr";

  currentUser: AppUser;
 
 
  constructor(public apiService: ApiserviceService,public utilsProvider:UtilsProviderService) {
    console.log('-------- INIT UserManagerProviderService Provider --------- ');
  }



  saveUser() {
    console.log("===== on sauve user ");
    Storage.set({ key: this.apiService.appName + '_currentUser', value: JSON.stringify(this.currentUser) });
    // sauve online full user
    this.apiService.putUser(this.currentUser).subscribe(done => {

    })
  }

  setUser(user) {
    let aUser = new User().initWithJSON(user);
    this.currentUser = aUser;
    console.log('User ID ' + aUser.id + ' email ' + aUser.email);
    console.log("=====cle " + this.apiService.appName + " on save user ");
    Storage.set({ key: this.apiService.appName + '_currentUser', value: JSON.stringify(user) });
  }


  getUser() {
    return new Promise(async resolve => {
      console.log("get User on cherche cle " + this.apiService.appName + '_currentUser')
      let result = await Storage.get({ key: this.apiService.appName + '_currentUser' });
      console.log(result)
      if (result.value) {
        //let user = JSON.parse(result);
        // console.log("on a trouve user pour cle "+JSON.stringify(result.value))
        let aUser = new AppUser().initWithJSON(JSON.parse(result.value));
        this.currentUser = aUser;
        resolve(this.currentUser)
      }
      else {
        console.log("Pas trouve cle pour get user")
        resolve()
      }

    });
  }

 
  logoutUser() {
    return new Promise(async resolve => {
      // on doit le passe offline
      console.log("-------- LOGOUT USER --------");


      this.currentUser = null;
      let result = await Storage.remove({ key: this.apiService.appName + '_currentUser' })
      resolve(true)

    });
  }
}
