import { ToastrService } from 'ngx-toastr';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { UsuarioService } from '../usuario.service';
import { JwtHelperService } from "@auth0/angular-jwt";
import { Router, RouterModule } from '@angular/router';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';

@Component({
  standalone: true,
  selector: 'app-user-login',
  styleUrls: ['./usuario-login.component.css'],
  templateUrl: './usuario-login.component.html',
  imports: [CommonModule, FormsModule, RouterModule, ReactiveFormsModule]
})

export class UsuarioLoginComponent implements OnInit {

  error: string = "";
  loginForm: FormGroup;
  intentoEnvio: boolean = false;
  helper = new JwtHelperService();

  constructor(
    private router: Router,
    private formBuilder: FormBuilder,
    private toastrService: ToastrService,
    private usuarioService: UsuarioService
  ) { this.loginForm = new FormGroup('') }

  ngOnInit() {
    sessionStorage.setItem('token', '');
    sessionStorage.setItem('idUsuario', '');
    sessionStorage.setItem('decodedToken', '');
    this.loginForm = this.formBuilder.group({
      username: ["", [Validators.required, Validators.maxLength(50)]],
      password: ["", [Validators.required, Validators.maxLength(50), Validators.minLength(4)]],
    });
  }

  loginUsuario(user = this.loginForm.get('username')?.value, password = this.loginForm.get('password')?.value) {

    this.error = "";
    this.intentoEnvio = true;
    
    if (this.loginForm.invalid) {
      return;
    }   

    this.usuarioService.login(user, password)
      .subscribe({
        next: (res) => {
          sessionStorage.setItem('decodedToken', JSON.stringify(this.helper.decodeToken(res.token)));
          sessionStorage.setItem('token', res.token);
          sessionStorage.setItem('idUsername', res.id);
          this.toastrService.success("Login ok", "Información", {closeButton: true});
          this.router.navigate([`/propiedades`]);
        },
        error: (err) => {
          this.error = "user o contraseña incorrectos";
          this.toastrService.error("Error al ingresar", "Error");
        }
      });
  }
}
