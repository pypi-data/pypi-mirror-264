# Mars Similarity Tools
A small tools library for getting vector similarity measurement working in no time.

# Example
Here's a basic similarity search and vectorization example. We instantiate a `VectorSimilarityService` which needs an `Augmentor` of some kind. The `Augmentor` should be responsible for taking objects inherited by `SimilarityObject` class and return vectorized grouped objects (as a `VectorGroup` object). Before a `SimilarityObject` can be transformed into a `VectorGroup` it will pass the `GroupParser` first. That one will rearrange the properties of the objects into groups, which is given in the parser. We need to do this since multiple properties of an object should in the end be represented by one vector together. 

```python
# First things first. Create a similarity model we want to measure similarity between
# And yes! You could create a seperate Color class that holds name and description for Color.
@dataclass(frozen=True) # Important!
class Bicycle(SimilarityObject):

    id: str
    color_name: str
    color_description: str
    wheel_size: int
    model: str

# Then create the parser, vectorizer, augmentor and service.
service = VectorSimilarityService(
    augmentor=ItemVectorizer(
        # NOTE! The default Vectorizer only returns random vectors.
        # So don't trust the similarity result here ;)
        vectorizer=Vectorizer(),
        parser=GroupParser(
            name=Bicycle.__class__.__name__, 
            children=[
                GroupParser(
                    name="color",
                    children=[
                        PropertyParser(
                            name="color name",
                            dtype=str,
                            path=["color_name"]
                        ),
                        PropertyParser(
                            name="color description",
                            dtype=str,
                            path=["color_description"]
                        ),
                    ],
                ),
                PropertyParser(
                    name="wheel_size",
                    dtype=int,
                    path=["wheel_size"]
                ),
                PropertyParser(
                    name="model",
                    dtype=str,
                    path=["model"]
                ),
            ]
        ),
    )
)

# Now we can create a namespace and add objects to that namespace.
namespace = "bicycles"
objects = [
    Bicycle(
        id="1",
        color_name="red",
        color_description="A red bicycle",
        wheel_size=26,
        model="mountain"
    ),
    Bicycle(
        id="2",
        color_name="blue",
        color_description="A blue bicycle",
        wheel_size=26,
        model="mountain"
    ),
    Bicycle(
        id="3",
        color_name="green",
        color_description="A green bicycle",
        wheel_size=28,
        model="racer"
    ),
]

# Create the namespace and add the objects to that namespace.
# It is because when we perform a similarity search, we need to know the objects to compare and
# so we bind the objects to a namespace.
service.create_namespace(namespace, objects)

# Now we can perform a similarity search.
similarity_result = service.similarity_search(
    namespace, 
    Bicycle(
        id="4",
        color_name="yellow",
        color_description="A yellow bicycle",
        wheel_size=28,
        model="racer"
    ), 
    top=2
)

# We could also do a similarity search including some bias to the search.
# For instance, we might want to find a similar bicycle but we want to bias the search
# towards the color.
biased_similarity_result = service.similarity_search(
    namespace, 
    Bicycle(
        id="4",
        color_name="yellow",
        color_description="A yellow bicycle",
        wheel_size=28,
        model="racer"
    ), 
    top=2,
    # Note here that we just say "color", so we select the common vector
    # for colors which from the group is both name and description for the color
    bias={"color": 1.2, "wheel_size": 0.2, "model": 0.2}
)
```