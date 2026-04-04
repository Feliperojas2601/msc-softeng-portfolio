import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule } from '@angular/forms';
import { UsuarioLoginComponent } from './usuario-login/usuario-login.component';
import { UsuarioRegistroComponent } from './usuario-registro/usuario-registro.component';

@NgModule({
  imports: [CommonModule, ReactiveFormsModule, UsuarioLoginComponent, UsuarioRegistroComponent],
  exports: [UsuarioLoginComponent, UsuarioRegistroComponent],
})

export class UsuarioModule { }
