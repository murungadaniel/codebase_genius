include supervisor;

walker codebase_genius {
    has url: str;

    # The ability MUST have a name: here it's `run`.
    can run with entry {
        if not self.url {
            report {
                "error": "Missing 'url' argument."
            };
            return;
        };

        sup = Supervisor();
        sup.url = self.url;

        report {
            "message": "Jac walker ran successfully.",
            "url": self.url
        };
    }
}
