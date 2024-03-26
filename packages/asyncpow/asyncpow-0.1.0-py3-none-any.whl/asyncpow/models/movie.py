"""
 AsyncPOW - https://github.com/totaldebug/asyncpow

 Copyright (c) 2024 Steven Marks, Total Debug

 Permission is hereby granted, free of charge, to any person obtaining a copy of
 this software and associated documentation files (the "Software"), to deal in
 the Software without restriction, including without limitation the rights to
 use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
 the Software, and to permit persons to whom the Software is furnished to do so,
 subject to the following conditions:

 The above copyright notice and this permission notice shall be included in all
 copies or substantial portions of the Software.

 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
 FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
 COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
 IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
 CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 """

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Genre:
    """
    Data class representing a movie genre.
    """

    id: int
    name: str


@dataclass
class Video:
    """
    Data class representing a video.
    """

    url: str
    key: str
    name: str
    size: int
    type: str
    site: str


@dataclass
class ProductionCompany:
    """
    Data class representing a production company.
    """

    id: int
    logoPath: str
    originCountry: str
    name: str


@dataclass
class ProductionCountry:
    """
    Data class representing a production country.
    """

    iso_3166_1: str
    name: str


@dataclass
class ReleaseDate:
    """
    Data class representing a release date.
    """

    certification: str
    iso_639_1: str
    note: str
    release_date: str
    type: int


@dataclass
class Cast:
    """
    Data class representing a cast member.
    """

    id: int
    castId: int
    character: str
    creditId: str
    gender: int
    name: str
    order: int
    profilePath: str


@dataclass
class Crew:
    """
    Data class representing a crew member.
    """

    id: int
    creditId: str
    gender: int
    name: str
    job: str
    department: str
    profilePath: str


@dataclass
class Collection:
    """
    Data class representing a collection.
    """

    id: int
    name: str
    posterPath: str
    backdropPath: str


@dataclass
class ExternalIds:
    """
    Data class representing external IDs.
    """

    facebookId: str
    freebaseId: str
    freebaseMid: str
    imdbId: str
    instagramId: str
    tvdbId: int
    tvrageId: int
    twitterId: str


@dataclass
class RequestedBy:
    """
    Data class representing the user who made the request.
    """

    id: int
    email: str
    username: str
    plexToken: str
    plexUsername: str
    userType: int
    permissions: int
    avatar: str
    createdAt: str
    updatedAt: str
    requestCount: int


@dataclass
class ModifiedBy:
    """
    Data class representing the user who modified the item.
    """

    id: int
    email: str
    username: str
    plexToken: str
    plexUsername: str
    userType: int
    permissions: int
    avatar: str
    createdAt: str
    updatedAt: str
    requestCount: int


@dataclass
class Request:
    """
    Data class representing a request.
    """

    id: int
    status: int
    media: str
    createdAt: str
    updatedAt: str
    requestedBy: RequestedBy
    modifiedBy: ModifiedBy
    is4k: bool
    serverId: int
    profileId: int
    rootFolder: str


@dataclass
class MediaInfo:
    """
    Data class representing media information.
    """

    id: int
    tmdbId: int
    tvdbId: int
    status: int
    requests: List[Request]
    createdAt: str
    updatedAt: str


@dataclass
class BuyFlatrate:
    """
    Data class representing a flatrate purchase option.
    """

    displayPriority: int
    logoPath: str
    id: int
    name: str


@dataclass
class WatchProvider:
    """
    Data class representing a watch provider.
    """

    iso_3166_1: str
    link: str
    buy: List[BuyFlatrate]
    flatrate: List[BuyFlatrate]


@dataclass
class MovieModel:
    """
    Data class representing a movie model.
    """

    id: int
    imdbId: str
    adult: bool
    backdropPath: str
    posterPath: str
    budget: int
    genres: List[Genre]
    homepage: str
    relatedVideos: List[Video]
    originalLanguage: str
    originalTitle: str
    overview: str
    popularity: float
    productionCompanies: List[ProductionCompany]
    productionCountries: List[ProductionCountry]
    releaseDate: str
    releases: dict
    revenue: int
    runtime: int
    spokenLanguages: List[str]
    status: str
    tagline: str
    title: str
    video: bool
    voteAverage: float
    voteCount: int
    credits: dict
    collection: Optional[Collection]
    externalIds: ExternalIds
    mediaInfo: MediaInfo
    watchProviders: List[List[WatchProvider]]
