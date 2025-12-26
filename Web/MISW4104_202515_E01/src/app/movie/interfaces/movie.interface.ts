export interface Movie {
    id: string;
    title: string;
    poster: string;
    duration: number;
    country: string;
    releaseDate: string;
    popularity: number;
    director: Director;
    actors: Actor[];
    genre: Genre;
    platforms: Platform[];
    reviews: Review[];
    youtubeTrailer: YoutubeTrailer;
}

export interface Director {
    id: string;
    name: string;
    photo: string;
    nationality: string;
    birthDate: string;
    biography: string;
}

export interface Actor {
    id: string;
    name: string;
    photo: string;
    nationality: string;
    birthDate: string;
    biography: string;
}

export interface Genre {
    id: string;
    type: string;
}

export interface Platform {
    id: string;
    name: string;
    url: string;
}

export interface Review {
    id: string;
    text: string;
    score: number;
    creator: string;
}

export interface YoutubeTrailer {
    id: string;
    name: string;
    url: string;
    duration: number;
    channel: string;
}
