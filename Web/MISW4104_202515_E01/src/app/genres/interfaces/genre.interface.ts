export interface Genre {
    id: string;
    type: string;
    movies: GenreMovie[];
}

export interface GenreMovie {
    id: string;
    title: string;
    poster: string;
    duration: number;
    country: string;
    releaseDate: string;
    popularity: number;
}
