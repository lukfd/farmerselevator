package main

import (
	"fmt"
	"log"
	"net/http"
)

/* PAGE HANDLERS */
// sign-in
func singinHandler(w http.ResponseWriter, r *http.Request) {
	template := `
	<h1>Farmers & Elevators</h1>
	<form action="/signin-form" method="post">
		<label>Username:</label>
		<input type="text" name="username"/>
		<label>Password:</label>
		<input type="password" name="password"/>
		<label>elevator?</label>
		<input type="checkbox" name="elevator"/>
		<button type="submit">sign-in</button>
	</form>`

	fmt.Fprintf(w, "%s", template)
}

func singinFormHandler(w http.ResponseWriter, r *http.Request) {
	// Call ParseForm() to parse the raw query and update r.PostForm and r.Form.
	if err := r.ParseForm(); err != nil {
		fmt.Fprintf(w, "ParseForm() err: %v", err)
		return
	}
	fmt.Fprintf(w, "Post from website! r.PostFrom = %v\n", r.PostForm)
	username := r.FormValue("username")
	password := r.FormValue("password")

	// check in DB

	// redirect to /home

	fmt.Fprintf(w, "user = %s\n", username)
	fmt.Fprintf(w, "pass = %s\n", password)
}

//sign-up
func singupHandler(w http.ResponseWriter, r *http.Request) {
	template := `
	<h1>Farmers & Elevators</h1>
	<form action="/signup-form" method="post">
		<label>Email:</label>
		<input type="email" name="email"/>
		<label>Username:</label>
		<input type="text" name="username"/>
		<label>Password:</label>
		<input type="password" name="password"/>
		<label>retype Password:</label>
		<input type="password"/>
		<label>elevator?</label>
		<input type="checkbox" name="elevator"/>
		<button type="submit">sign-up</button>
	</form>`

	fmt.Fprintf(w, "%s", template)
}

func singupFormHandler(w http.ResponseWriter, r *http.Request) {
	// Call ParseForm() to parse the raw query and update r.PostForm and r.Form.
	if err := r.ParseForm(); err != nil {
		fmt.Fprintf(w, "ParseForm() err: %v", err)
		return
	}
	fmt.Fprintf(w, "Post from website! r.PostFrom = %v\n", r.PostForm)
	name := r.FormValue("name")
	address := r.FormValue("address")
	fmt.Fprintf(w, "Name = %s\n", name)
	fmt.Fprintf(w, "Address = %s\n", address)
}

// home
func homeHandler(w http.ResponseWriter, r *http.Request) {
	template := `
	<h1>Farmers & Elevators</h1>
	`

	fmt.Fprintf(w, "%s", template)
}

/* MAIN */
func main() {
	// static server
	fileServer := http.FileServer(http.Dir("./public"))
	http.Handle("/", fileServer)

	// other webpage request
	http.HandleFunc("/signin", singinHandler)
	http.HandleFunc("/signin-form", singinFormHandler)
	http.HandleFunc("/signup", singupHandler)
	http.HandleFunc("/signup-form", singupFormHandler)
	http.HandleFunc("/home", homeHandler)

	// starting server...
	fmt.Printf("Starting server at port 8080\n")
	if err := http.ListenAndServe(":8080", nil); err != nil {
		log.Fatal(err)
	}
}
