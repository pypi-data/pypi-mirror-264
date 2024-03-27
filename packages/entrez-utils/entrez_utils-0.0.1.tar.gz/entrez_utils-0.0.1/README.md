# entrez_utils

This library allows you to access information in remote Entrez databases from 
Python.

## Examples

### Creating an `EntrezManager`

An `EntrezManager` controls communication with the Entrez databases via HTTP
requests. The class is aware of the methods supported by the Entrez API and
ensures that the rate limits are not exceeded.

NCBI requests that the email address of the user be sent with requests, so an
email is required to construct an `EntrezManager`.

```python
from entrez_utils import EntrezManager

man = EntrezManager("foo@example.com")
```

### Accessing a record

Most objects can be constructed with either an accession or an Entrez ID.

```python
from entrez_utils import BioProject, BioSample, SRAExperiment, SRARun

project = BioProject(man, accession="PRJNA293777")
sample = BioSample(man, entrez_id="4009779")
experiment = SRAExperiment(man, accession="SRX4958339")
run = SRARun(man, accession="SRR8137396	")
```

### Getting linked records

Properties of a record can be used to get other linked records. For example, 
this code gets the samples associated with a project.

```python
samples = project.samples
```

### Accessing raw XML

The Python objects representing Entrez records do not expose all possible data
from the XML through their properties. The `xml` attribute give access to a 
parsed version of the raw XML associated with the record.

```python
xml = project.xml
```

### Batch fetching objects

The XML for a record is ordinarily retrieved lazily, but separately fetching
XML for many records can be time consuming. To speed up the process, you can
use `fetch_all` to fetch many records' XML at once.

```python
samples = project.samples
fetch_all(samples)
```

The `fetched` function runs `fetch_all` on its argument and returns the
argument, so it can be used to make the code above more concise.

```python
samples = fetched(project.sample)
```
