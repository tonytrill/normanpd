# !/usr/bin/env python3
# -*- coding: utf-8 -*-
import normanpd
from normanpd import normanpd


def main():

    # Gets the PDFs from the URL
    normanpd.fetchincidents()

    # Gets the data
    incidents = normanpd.extractincidents()

    # Creates the database
    normanpd.createdb()

    # Populate database
    normanpd.populatedb(incidents)

    # Print status
    normanpd.status(incidents)

if __name__ == "__main__":
    main()

