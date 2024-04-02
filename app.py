from application import app

if __name__ == "__main__":  # This conditional block checks if the script is being run directly by Python
    # When a Python script is executed, Python sets the special variable __name__ to "__main__" if it is
    # the main script being run.
    app.run(debug=True)
    # This method starts the Flask development server to serve the application. the parameter enables debug mode, which
    # provides helpful debugging information and automatically restarts the server when code changes are detected.
    # It's useful during development but should be disabled in production.
