export interface Actor {
    id: string;
    name: string;
    photo: string;
    nationality: string;
    birthDate: string;
    biography: string;
    movies: ActorMovie[];
}

export interface ActorMovie {
    id: string;
    title: string;
    poster: string;
    duration: number;
    country: string;
    releaseDate: string;
    popularity: number;
}
