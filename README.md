# buildots-home-assignment
This is a home assignment for the buildots company interview


## design
The Service class is a subclass of Process and can be started and stopped from a calling main thread.
Every service (Projector, ImageDownloader, etc.) inherits from Service.
Every service has am input directory, an iterable of output directories and a FilePoller.

The FilePoller is initialized with a target directory and uses polling every _interval_ seconds to read the files from the directory and look for any new files. New files are pushed into a task queue that is read in the main loop of every process and within is a call to process_file and then delete_file when done.

## More comments
I left comments in various places noting what I'd do differently if I had more time