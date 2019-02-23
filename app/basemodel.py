from app import db
from flask import json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm.attributes import QueryableAttribute

class Base(db.Model):
    __abstract__ = True

    def to_dict(self, show=None, _hide=[], _path=None):
        """Return a dictionary representation of this model."""

        show = show or []

        hidden = self._hidden_fields if hasattr(self, "_hidden_fields") else []
        default = self._default_fields if hasattr(self, "_default_fields") else []
        default.extend(['id', 'modified_at', 'created_at'])

        if not _path:
            _path = self.__tablename__.lower()

            def prepend_path(item):
                item = item.lower()
                if item.split(".", 1)[0] == _path:
                    return item
                if len(item) == 0:
                    return item
                if item[0] != ".":
                    item = ".%s" % item
                item = "%s%s" % (_path, item)
                return item

            _hide[:] = [prepend_path(x) for x in _hide]
            show[:] = [prepend_path(x) for x in show]

        columns = self.__table__.columns.keys()
        properties = dir(self)

        ret_data = {}

        for key in columns:
            if key.startswith("_"):
                continue
            check = "%s.%s" % (_path, key)
            if check in _hide or key in hidden:
                continue
            if check in show or key in default:
                ret_data[key] = getattr(self, key)

        for key in list(set(properties) - set(columns)):
            if key.startswith("_"):
                continue
            if not hasattr(self.__class__, key):
                continue
            attr = getattr(self.__class__, key)
            if not (isinstance(attr, property)
                    or isinstance(attr, QueryableAttribute)):
                continue
            check = "%s.%s" % (_path, key)
            if check in _hide or key in hidden:
                continue
            if check in show or key in default:
                val = getattr(self, key)
                if hasattr(val, "to_dict"):
                    ret_data[key] = val.to_dict(
                        show=list(show),
                        _hide=list(_hide), #_path=("%s.%s" % (_path, key.lower()))
                        _path=('%s.%s' % (path, key.lower()))#,
                    )
                else:
                    try:
                        ret_data[key] = json.loads(json.dumps(val))
                    except:
                        pass

        return ret_data

    def from_dict(self, **kwargs):
        """Update this model with a dictionary."""
        _force = kwargs.pop("_force", False)

        readonly = self._readonly_fields if hasattr(self, "_readonly_fields") \
            else []
        # if hidden_fields list defined append to readonly list
        if hasattr(self, "_hidden_fields"):
            readonly += self._hidden_fields
        # force id, created_at and modified_at as readonly
        readonly += ["id", "created_at", "modified_at"]
        print("read only {}".format(readonly))
        # read table column keys
        columns = self.__table__.columns.keys()
        print("columns {}".format(columns))
        # list of valid attributes of the object
        properties = dir(self)
        #define empty dict to store changes in th db
        changes = {}
        # iterate keys in columns
        for key in columns:
            # ignore special keys
            if key.startswith("_"):
                continue
            # if key is editable = not in readonly list
            allowed = True if _force or key not in readonly else False
            # is column key listed in kwargs
            exists = True if key in kwargs else False
            if allowed and exists:
                # get current table value for the key
                val = getattr(self, key)
                if val != kwargs[key]:
                    # no point in updating to the same value
                    changes[key] = {"old": val, "new": kwargs[key]}
                    # set column current row value
                    setattr(self, key, kwargs[key])

        for key in list(set(properties) - set(columns)):
            if key.startswith("_"):
                continue
            allowed = True if _force or key not in readonly else False
            exists = True if key in kwargs else False
            if allowed and exists and getattr(self.__class__, key).fset is not None:
                val = getattr(self, key)
                if hasattr(val, "to_dict"):
                    val = val.to_dict()
                changes[key] = {"old": val, "new": kwargs[key]}
                setattr(self, key, kwargs[key])

        return changes
