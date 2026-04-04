import { Router } from '@angular/router';
import { ToastrService } from 'ngx-toastr';
import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { UsuarioService } from '../usuario.service';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';

@Component({
  standalone: true,
  selector: 'app-usuario-registro',
  imports: [CommonModule, ReactiveFormsModule],
  styleUrls: ['./usuario-registro.component.css'],
  templateUrl: './usuario-registro.component.html'
})

export class UsuarioRegistroComponent implements OnInit {

  error: string = "";
  usuarioForm: FormGroup;

  constructor(
    private router: Router,
    private formBuilder: FormBuilder,
    private toastrService: ToastrService,
    private usuarioService: UsuarioService
  ) { this.usuarioForm = new FormGroup('') }

  ngOnInit() {
    this.usuarioForm = this.formBuilder.group({
      role: ["", [Validators.required, Validators.maxLength(15)]],
      username: ["", [Validators.required, Validators.maxLength(50)]],
      password: ["", [Validators.required, Validators.maxLength(50), Validators.minLength(4)]],
      confirmPassword: ["", [Validators.required, Validators.maxLength(50), Validators.minLength(4)]]
    });
  }

  registroUsuario() {
    this.usuarioService.registro(this.usuarioForm.get('username')?.value, this.usuarioForm.get('role')?.value, this.usuarioForm.get('password')?.value)
      .subscribe({
        next: (res) => {
          this.toastrService.success("Registro exitoso");
          this.router.navigate([`/`]);
      },
      error: (res) => {
        this.toastrService.error("Error en el registro. Verifique que el usuario no se encuentre ya registrado", "Error", {closeButton: true});
      }
    });
  }
}