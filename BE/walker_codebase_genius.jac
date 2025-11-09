walker codebase_genius {
    has url: str = "";

    obj __specs__ {
        static has auth: bool = False;
    }

    can execute with root entry {
        if not self.url or "github.com" not in self.url {
            report {"error": "Valid GitHub URL with .git required."};
            disengage;
        }

        supervisor = Supervisor(url=self.url);
        root ++> supervisor;
        visit supervisor;
    }
}