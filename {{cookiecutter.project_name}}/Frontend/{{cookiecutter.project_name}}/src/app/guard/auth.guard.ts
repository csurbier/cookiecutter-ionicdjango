import { Injectable } from '@angular/core';
import { CanActivate } from '@angular/router';
import { AuthentificationProviderService } from '../service/authentification-provider.service';
 
@Injectable({
  providedIn: 'root'
})
export class AuthGuard implements CanActivate {
 
  constructor(public auth: AuthentificationProviderService) {}
 
  canActivate(): boolean {
    return this.auth.isAuthenticated();
  }
}