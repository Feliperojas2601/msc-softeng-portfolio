import { faker } from '@faker-js/faker';

export class DataGenerators {
    static generateActor() {
        const firstName = faker.person.firstName();
        const lastName = faker.person.lastName();
        const birthdate = faker.date.birthdate({
            min: 1940,
            max: 2005,
            mode: 'year',
        });

        return {
            name: `${firstName} ${lastName}`,
            photo: faker.image.avatar(),
            nationality: faker.location.country(),
            birthDate: birthdate.toISOString().split('T')[0],
            biography: faker.lorem.paragraph(),
        };
    }

    static generateDirector() {
        const firstName = faker.person.firstName();
        const lastName = faker.person.lastName();
        const birthdate = faker.date.birthdate({
            min: 1940,
            max: 1990,
            mode: 'year',
        });

        return {
            name: `${firstName} ${lastName}`,
            photo: faker.image.avatar(),
            nationality: faker.location.country(),
            birthDate: birthdate.toISOString().split('T')[0],
            biography: faker.lorem.paragraph(),
        };
    }

    static generateGenre() {
        const genres = [
            'Ciencia Ficción',
            'Drama',
            'Terror',
            'Comedia',
            'Acción',
            'Aventura',
            'Thriller',
            'Romance',
            'Fantasía',
            'Documental',
            'Musical',
            'Animación',
        ];

        const randomGenre = faker.helpers.arrayElement(genres);
        const uniqueSuffix = faker.string.alphanumeric(4);

        return {
            type: `${randomGenre} ${uniqueSuffix}`,
            // Alias for backward compatibility
            name: `${randomGenre} ${uniqueSuffix}`,
            description: faker.lorem.sentence(),
        };
    }

    static generateMovie() {
        const title = faker.commerce.productName();
        const releaseDate = faker.date.past({ years: 20 });

        return {
            title: `${title} ${faker.string.alphanumeric(4)}`,
            poster: faker.image.url({ width: 300, height: 450 }),
            duration: faker.number.int({ min: 80, max: 180 }),
            country: faker.location.country(),
            releaseDate: releaseDate.toISOString().split('T')[0],
            popularity: faker.number.float({
                min: 1,
                max: 10,
                fractionDigits: 1,
            }),
        };
    }

    static generateInvalidActor() {
        return {
            name: '', // Empty name
            photo: 'invalid-url',
            nationality: faker.location.country(),
            birthDate: 'invalid-date',
            biography: faker.lorem.paragraph(),
        };
    }

    static generateInvalidDirector() {
        return {
            name: '', // Empty name
            photo: 'invalid-url',
            nationality: faker.location.country(),
            birthDate: 'invalid-date',
            biography: faker.lorem.paragraph(),
        };
    }

    static generateInvalidGenre() {
        return {
            type: '', // Empty type
        };
    }

    static generateInvalidMovie() {
        return {
            title: '', // Empty title
            poster: 'invalid-url',
            duration: -10, // Negative duration
            country: faker.location.country(),
            releaseDate: 'invalid-date',
            popularity: 15, // Out of range
        };
    }

    static generateActors(count: number = 5) {
        return Array.from({ length: count }, () => this.generateActor());
    }

    static generateDirectors(count: number = 5) {
        return Array.from({ length: count }, () => this.generateDirector());
    }

    static generateGenres(count: number = 5) {
        return Array.from({ length: count }, () => this.generateGenre());
    }

    static generateMovies(count: number = 5) {
        return Array.from({ length: count }, () => this.generateMovie());
    }

    static generateNonExistentSearchTerm() {
        return `NOTFOUND_${faker.string.alphanumeric(10)}`;
    }

    static generateRandomYear() {
        return faker.number.int({ min: 1980, max: 2024 });
    }

    static generateReviewText() {
        return faker.lorem.paragraph({ min: 2, max: 4 });
    }

    static generateRating() {
        return faker.number.int({ min: 1, max: 5 });
    }

    static generatePersonName() {
        const firstName = faker.person.firstName();
        const lastName = faker.person.lastName();
        return `${firstName} ${lastName}`;
    }
}
