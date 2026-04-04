export class Usuario {
    username: string;
    role: string
    password: string;

    public constructor(username: string, role: string, password:string) {
        this.username = username
        this.role = role
        this.password = password
    }
}
