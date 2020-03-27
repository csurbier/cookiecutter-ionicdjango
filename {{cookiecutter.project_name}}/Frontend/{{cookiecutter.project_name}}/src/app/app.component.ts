import { Component } from '@angular/core';
import { Platform } from '@ionic/angular';
import { ApiserviceService, ConnectionStatus } from './service/apiservice.service'

import {
  Plugins,
  StatusBarStyle,
} from '@capacitor/core';
import { Router } from '@angular/router';
import { NavDataServiceService } from './service/nav-data-service.service';
import { UserManagerProviderService } from './service/user-manager-provider.service';
import { UtilsProviderService } from './service/utils-provider';
import { AuthentificationProviderService } from './service/authentification-provider.service';
import { BehaviorSubject } from 'rxjs';
import { ScreenOrientation } from '@ionic-native/screen-orientation/ngx';
import { AppUser } from './models/entities.ts';
const { StatusBar } = Plugins;
@Component({
  selector: 'app-root',
  templateUrl: 'app.component.html',
  styleUrls: ['app.component.scss']
})
export class AppComponent {
  userConnected = true; 

  constructor(
    private platform: Platform,
    public apiService: ApiserviceService,
    public router: Router,
    public navDataService: NavDataServiceService,
    public userManager: UserManagerProviderService,
    public utilsProvider: UtilsProviderService,
    private screenOrientation: ScreenOrientation,
    public authentificationService: AuthentificationProviderService) {
    this.initializeApp();
  }
 
  initializeApp() {
    this.platform.ready().then(() => {
      if (this.platform.is("cordova")) {
        this.screenOrientation.lock(this.screenOrientation.ORIENTATIONS.PORTRAIT);
   
        StatusBar.setStyle({
          style: StatusBarStyle.Dark
        });

      }
      
      //   this.splashScreen.hide();
      //Subscribe on resume
      this.platform.resume.subscribe(() => {
        
        if (this.userConnected) {
          
          this.authentificationService.authenticationState.next(true)

          this.changeStatus(true);

        }
      });

      // Quit app
      this.platform.pause.subscribe(() => {
        if (this.userConnected) {
          this.goOffline();

        }
      });
      // Path dans url ?
      if (document.URL.length > 0) {
        // let index = document.URL.indexOf('/') + 1
        let lastPath = window.location.pathname
        console.log("index PATH recu " + lastPath + " on va donc directement sur la page ?")
        if (lastPath.length > 1) {
          console.log("======= navigateByUrl /" + lastPath)
          this.loadTokenAndGoToPage("/" + lastPath)
        }
        else {
          console.log("Arrive à la racine du site")
          this.loadTokenAndGoToPage("/")
        }
      }

    });
  }
 

  accessAuthorizedWithUrl(goToUrl) {
    // On passe toujours par l'ecran d'accueil
    console.log("Token ok on peut downloader data")
    setTimeout( () => {
      // somecode
     this.router.navigateByUrl("/home")
    }, 400);
   
    
  }

  loadTokenAndGoToPage(url) {
    this.apiService.checkOauthToken().then((result) => {
      if (result) {
        console.log("ACCESS DIRECT  Deja token " + result);
        this.accessAuthorizedWithUrl(url)
      }
      else {

        console.log("ACCESS DIRECT PAS DE TOKEN TOKEN")
        this.getToken(url)
      }
    });
  }

  getToken(url) {
    console.log("Pas deja token ")
    this.apiService.checkOauthToken().then((token) => {
      if (token) {
        console.log("Retour WS token " + token + " on sauve token en local " + token)
        this.authentificationService.authenticationState.next(true)
        this.accessAuthorizedWithUrl(url)
      }
      else {
        // Get token
        this.apiService.getOAuthToken().then((token) => {
          if (token) {
            console.log("Retour WS token " + token + " on sauve token en local " + token)
            this.authentificationService.authenticationState.next(true)
            this.accessAuthorizedWithUrl(url)
          }
          else {
            console.log("ERREUR RETOUR TOKEN");
            this.authentificationService.authenticationState.next(false)
            this.apiService.showError("Impossible de communiquer avec nos serveurs.");

          }
        });
      }
    });
  }



  changeStatus(online) {
    console.log("ON CHANGE STATUS " + online);

    let patchParams = {
      "lastConnexionDate": new Date(),
      "online": online
    }
    // let id="1543898c-bb3c-4a60-a9bc-4c1595bc5c1b"
    // this.apiService.patchUserCS(id,patchParams).subscribe((resultat)=>{
    // });

    if (this.userManager.currentUser) {
      try {
        this.apiService.patchUser(this.userManager.currentUser.id, patchParams).subscribe((resultat) => {
        });
      }
      catch{
        console.log("catch")
      }
    }
  }

  goOffline() {
    
  }

  refreshFiles() {
    // this.files = this.imageFileProvider.fichiers;
  }


}
