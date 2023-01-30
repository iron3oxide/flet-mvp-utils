# flet-mvp-utils

WIP, not complete!

This library provides tools that make it a bit easier
to follow architecture patterns in your flet app
that leverage on immutable models and unidirectional control flow.
Those are mostly based on the Model-View-Presenter/MVP pattern,
hence the name of the library.
At this stage,
it can be used to ease working with any model-based architecture pattern though.

## Usage

Say you have a form and want to validate the TextFields in it
when a submit button is clicked.

Your view uses [refs](https://flet.dev/docs/guides/python/control-refs/).
The actual UI code may be located somewhere else
and simply receive the refs and return a component that is connected to the ref.
When creating the view class, you inherit from `MvpView`
and in your `__init__.py`, you create a dictionary that maps the attribute names
of your model to the respective ref
of the control that should be tied to it.
You then pass this dictionary to `super().__init__()`,
along with any variable intended for the `flet.View` constructor.

```python
```

`MvpView` has a `render(model)` method that takes a model
and updates any refs current value to the model value if they aren't the same.
This method is supposed to be called in the callback
you register with the data source,
so that a changed model is immediately reflected in the view.

Your model inherits from `MvpModel`,
which is an immutable pydantic BaseModel.
This means you can write custom validators for each attribute
and validate all your data whenever a new instance of the model is created.

```python
class FormModel(MvpModel):
    number: int = 0
```

The business logic of your component/virtual page
will live in a DataSource class which inherits from `MvpDataSource`.
Since the latter inherits from `Observable`,
brokers of any kind (presenter classes in MVP-based architectures)
can register callback functions with your DataSource class
that will be executed when you call `self.notify_observers()` in it.

This is meant to be used to inform the presenter that a new,
updated model has been created.
Since creating and updating a model is a rather repetitive and uniform task,
`MvpDataSource` will do it for you.
All you have to do is pass your model class to its constructor
and call `self.update_model_partial(changes: dict)`
or `self.update_model_complete(new_model: dict)` depending on your use case.
