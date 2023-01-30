# flet-mvp-utils

This library provides tools that make it a bit easier
to follow architecture patterns in your flet app
that leverage on immutable models and unidirectional control flow.
Those are mostly based on the Model-View-Presenter/MVP pattern,
hence the name of the library.
At this stage,
it can be used to ease working with any model-based architecture pattern though.

## Assumptions/usage

Your model inherits from MvpModel,
which is an immutable pydantic BaseModel.
Some kind of broker is subscribed to be notified of
any change of the current model of e.g. the data source that holds
and modifies it/creates updated models.
This is done with the help of the `Observable` class.
The data source inherits from it,
the broker (or presenter in MVP terms) registers a callback with it
and when the data source updates/replaces its model,
it notifies the presenter (and other subscribed observers).

Your view uses [refs](https://flet.dev/docs/guides/python/control-refs/).
The actual UI code may be located somewhere else
and simply receive the refs and return a component that is connected to the ref.
When creating the view class, you inherit from `MvpView`
and in your `__init__.py`, you create a dictionary that maps the attribute names
of your model dataclass to the respective ref
of the control that should be tied to it.
You then pass this dictionary to `super().__init__()`,
along with any variable intended for the `flet.View` constructor.
`MvpView` has a `render(model)` method that takes a model
and updates any refs current value to the model value if they aren't the same.
This method is supposed to be called in the callback
you register with the data source,
so that a changed model is immediately reflected in the view.
