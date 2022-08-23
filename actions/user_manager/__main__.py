import nuvolaris.config as cfg
import nuvolaris.couchdb_util as cu

def test(db):
    db.create_db("test")
    doc = {"_id":"test", "value":"hello" }
    db.update_doc("test",  doc)
    return db.get_doc("test", "test")

def main(args):
    cfg.clean()
    cfg.put("couchdb.host", args['couchdb_host'])
    cfg.put("couchdb.admin.user", args['couchdb_user'])
    cfg.put("couchdb.admin.password", args['couchdb_password'])
    db = cu.CouchDB()
    return {
        "body": test(db)
    }
