# Philosophy — REST Pack

REST's value is predictability through convention: resources as nouns, HTTP verbs as the uniform action vocabulary, status codes as a standardized outcome signal. A consumer who's used one well-designed REST API can guess most of another's shape correctly — that transferable predictability is the entire point, and it's lost the moment an API invents its own verbs-in-URLs (`/getUser`) or repurposes status codes inconsistently (`200 OK` with an error body).
