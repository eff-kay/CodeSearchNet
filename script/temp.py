from functools import reduce
def run_blockstackd():
    """
    run blockstackd
    """
    special_args, new_argv = check_and_set_envars( sys.argv )
    working_dir = special_args.get('working_dir')
    if working_dir is None:
        working_dir = os.path.expanduser('~/.{}'.format(virtualchain_hooks.get_virtual_chain_name()))
        
    # if we're in a testnet, then make sure we're in the testnet-specific working directory 
    if BLOCKSTACK_TESTNET_ID is not None:
        working_dir = os.path.join(working_dir, 'testnet', BLOCKSTACK_TESTNET_ID)
        log.info('Using testnet {}, chain state in {}'.format(BLOCKSTACK_TESTNET_ID, working_dir))

    setup(working_dir)

    # need sqlite3
    sqlite3_tool = virtualchain.sqlite3_find_tool()
    if sqlite3_tool is None:
        print('Failed to find sqlite3 tool in your PATH.  Cannot continue')
        sys.exit(1)
    
    argparser = argparse.ArgumentParser()

    # get RPC server options
    subparsers = argparser.add_subparsers(
        dest='action', help='the action to be taken')
     
    # -------------------------------------
    parser = subparsers.add_parser(
        'start',
        help='start blockstackd')
    parser.add_argument(
        '--foreground', action='store_true',
        help='start blockstackd in foreground')
    parser.add_argument(
        '--expected-snapshots', action='store')
    parser.add_argument(
        '--expected_snapshots', action='store',
        help='path to a .snapshots file with the expected consensus hashes')
    parser.add_argument(
        '--port', action='store',
        help='peer network port to bind on')
    parser.add_argument(
        '--api-port', action='store')
    parser.add_argument(
        '--api_port', action='store',
        help='RESTful API port to bind on')
    parser.add_argument(
        '--working-dir', action='store',
        help='Directory with the chain state to use')
    parser.add_argument(
        '--no-indexer', action='store_true',
        help='Do not start the indexer component')
    parser.add_argument(
        '--indexer_url', action='store'),
    parser.add_argument(
        '--indexer-url', action='store',
        help='URL to the indexer-enabled blockstackd instance to use')
    parser.add_argument(
        '--no-api', action='store_true',
        help='Do not start the RESTful API component')
    parser.add_argument(
        '--genesis_block', action='store',
        help='Path to an alternative genesis block source file')
    parser.add_argument(
        '--signing_key', action='store',
        help='GPG key ID for an alternative genesis block')

    # -------------------------------------
    parser = subparsers.add_parser(
        'stop',
        help='stop the blockstackd server')
    parser.add_argument(
        '--working-dir', action='store',
        help='Directory with the chain state to use')

    # -------------------------------------
    parser = subparsers.add_parser(
        'configure',
        help='reconfigure the blockstackd server')
    parser.add_argument(
        '--working-dir', action='store',
        help='Directory with the chain state to use')

    # -------------------------------------
    parser = subparsers.add_parser(
        'clean',
        help='remove all blockstack database information')
    parser.add_argument(
        '--force', action='store_true',
        help='Do not confirm the request to delete.')
    parser.add_argument(
        '--working-dir', action='store',
        help='Directory with the chain state to use')

    # -------------------------------------
    parser = subparsers.add_parser(
        'restore',
        help="Restore the database from a backup")
    parser.add_argument(
        'block_number', nargs='?',
        help="The block number to restore from (if not given, the last backup will be used)")
    parser.add_argument(
        '--working-dir', action='store',
        help='Directory with the chain state to use')

    # -------------------------------------
    parser = subparsers.add_parser(
        'verifydb',
        help='verify an untrusted database against a known-good consensus hash')
    parser.add_argument(
        'block_height',
        help='the block height of the known-good consensus hash')
    parser.add_argument(
        'consensus_hash',
        help='the known-good consensus hash')
    parser.add_argument(
        'chainstate_dir',
        help='the path to the database directory to verify')
    parser.add_argument(
        '--expected-snapshots', action='store',
        help='path to a .snapshots file with the expected consensus hashes')
    parser.add_argument(
        '--working-dir', action='store',
        help='Directory with the chain state to use')

    # -------------------------------------
    parser = subparsers.add_parser(
        'version',
        help='Print version and exit')

    # -------------------------------------
    parser = subparsers.add_parser(
        'fast_sync',
        help='fetch and verify a recent known-good name database')
    parser.add_argument(
        'url', nargs='?',
        help='the URL to the name database snapshot')
    parser.add_argument(
        'public_keys', nargs='?',
        help='a CSV of public keys to use to verify the snapshot')
    parser.add_argument(
        '--num_required', action='store',
        help='the number of required signature matches')
    parser.add_argument(
        '--working-dir', action='store',
        help='Directory with the chain state to use')

    # -------------------------------------
    parser = subparsers.add_parser(
        'fast_sync_snapshot',
        help='make a fast-sync snapshot')
    parser.add_argument(
        'private_key',
        help='a private key to use to sign the snapshot')
    parser.add_argument(
        'path',
        help='the path to the resulting snapshot')
    parser.add_argument(
        'block_height', nargs='?',
        help='the block ID of the backup to use to make a fast-sync snapshot')
    parser.add_argument(
        '--working-dir', action='store',
        help='Directory with the chain state to use')

    # -------------------------------------
    parser = subparsers.add_parser(
        'fast_sync_sign',
        help='sign an existing fast-sync snapshot')
    parser.add_argument(
        'path', action='store',
        help='the path to the snapshot')
    parser.add_argument(
        'private_key', action='store',
        help='a private key to use to sign the snapshot')
    parser.add_argument(
        '--working-dir', action='store',
        help='Directory with the chain state to use')

    # -------------------------------------
    parser = subparsers.add_parser(
        'audit',
        help='audit the genesis block')
    parser.add_argument(
        '--path', action='store',
        help='Alternative path to a genesis block')
    parser.add_argument(
        '--signing_key', action='store',
        help='GPG key ID that signed the genesis block')
    parser.add_argument(
        '--working-dir', action='store',
        help='Directory with the chain state to use')

    # -------------------------------------
    parser = subparsers.add_parser(
        'db_version',
        help='Get the chain state database version.  Exit 0 if the database is compatible with this node, and exit 1 if not.')
    parser.add_argument(
        '--working-dir', action='store',
        help='Directory with the chain state to use')

    args, _ = argparser.parse_known_args(new_argv[1:])

    if args.action == 'version':
        print("Blockstack version: %s" % VERSION)
        sys.exit(0)

    if args.action == 'db_version':
        db_path = virtualchain.get_db_filename(virtualchain_hooks, working_dir)
        if os.path.exists(db_path):
            ver = chainstate.namedb_read_version(db_path)
            print("{}".format(ver))

            if semver_equal(ver, VERSION):
                sys.exit(0)
            else:
                sys.exit(1)

        else:
            print("No chainstate db found at {}".format(db_path))
            sys.exit(1)

    elif args.action == 'start':
        # db state must be compatible
        db_path = virtualchain.get_db_filename(virtualchain_hooks, working_dir)
        if os.path.exists(db_path):
            ver = chainstate.namedb_read_version(db_path)
            if not semver_equal(ver, VERSION):
                print('FATAL: this node is version {}, but the chainstate db is version {}.  Please upgrade your chainstate db by either using the `fast_sync` command or re-indexing the blockchain.'.format(VERSION, ver), file=sys.stderr)
                sys.exit(1)

        expected_snapshots = {}

        pid = read_pid_file(get_pidfile_path(working_dir))
        still_running = False
       
        use_api = None
        use_indexer = None
        if args.no_api:
            use_api = False

        if args.no_indexer:
            use_indexer = False

        if pid is not None:
           try:
               still_running = check_server_running(pid)
           except:
               log.error("Could not contact process {}".format(pid))
               sys.exit(1)
       
        if still_running:
           log.error("Blockstackd appears to be running already.  If not, please run '{} stop'".format(sys.argv[0]))
           sys.exit(1)

        # alternative genesis block?
        if args.genesis_block:
            log.info('Using alternative genesis block {}'.format(args.genesis_block))
            if args.signing_key:
                # audit it
                res = do_genesis_block_audit(genesis_block_path=args.genesis_block, key_id=args.signing_key)
                if not res:
                    print('Genesis block {} is INVALID'.format(args.genesis_block), file=sys.stderr)
                    sys.exit(1)

            else:
                # don't audit it, but instantiate it
                genesis_block_load(args.genesis_block)

        # unclean shutdown?
        is_indexing = BlockstackDB.db_is_indexing(virtualchain_hooks, working_dir)
        if is_indexing:
            log.warning('Unclean shutdown detected!  Will attempt to restore from backups')

        recover = False
        if pid is not None and use_indexer is not False or is_indexing:
           # The server didn't shut down properly.
           # restore from back-up before running
           log.warning("Server did not shut down properly (stale PID {}, or indexing lockfile detected).  Restoring state from last known-good backup.".format(pid))

           # move any existing db information out of the way so we can start fresh.
           state_paths = BlockstackDB.get_state_paths(virtualchain_hooks, working_dir)
           need_backup = reduce( lambda x, y: x or y, [os.path.exists(sp) for sp in state_paths], False )
           if need_backup:

               # have old state.  keep it around for later inspection
               target_dir = os.path.join( working_dir, 'crash.{}'.format(time.time()))
               os.makedirs(target_dir)
               for sp in state_paths:
                   if os.path.exists(sp):
                      target = os.path.join( target_dir, os.path.basename(sp) )
                      shutil.move( sp, target )

               log.warning("State from crash stored to '{}'".format(target_dir))

           blockstack_backup_restore(working_dir, None)

           # make sure we "stop"
           set_indexing(working_dir, False)
           BlockstackDB.db_set_indexing(False, virtualchain_hooks, working_dir)

           # just did a recovery; act accordingly
           setup_recovery(working_dir)

        # use snapshots?
        if args.expected_snapshots is not None:
           expected_snapshots = load_expected_snapshots( args.expected_snapshots )
           if expected_snapshots is None:
               sys.exit(1)
        else:
           log.debug("No expected snapshots given")

        # we're definitely not running, so make sure this path is clear
        try:
           os.unlink(get_pidfile_path(working_dir))
        except:
           pass

        if args.foreground:
           log.info('Initializing blockstackd server in foreground (working dir = \'%s\')...' % (working_dir))
        else:
           log.info('Starting blockstackd server (working_dir = \'%s\') ...' % (working_dir))

        if args.port is not None:
           log.info("Binding on port %s" % int(args.port))
           args.port = int(args.port)
        else:
           args.port = None

        if args.api_port is not None:
            log.info('Binding RESTful API on port {}'.format(int(args.api_port)))
            args.api_port = int(args.api_port)
        else:
            args.api_port = None

        recover = check_recovery(working_dir)
        exit_status = run_server(working_dir, foreground=args.foreground, expected_snapshots=expected_snapshots, port=args.port, api_port=args.api_port, use_api=use_api, use_indexer=use_indexer, indexer_url=args.indexer_url, recover=recover)
        if args.foreground:
           log.info("Service endpoint exited with status code %s" % exit_status )

    elif args.action == 'stop':
        stop_server(working_dir, kill=True)

    elif args.action == 'configure':
        reconfigure(working_dir)

    elif args.action == 'restore':
        block_number = args.block_number
        if block_number is not None:
          block_number = int(block_number)

        pid = read_pid_file(get_pidfile_path(working_dir))
        still_running = False
       
        if pid is not None:
           try:
               still_running = check_server_running(pid)
           except:
               log.error("Could not contact process {}".format(pid))
               sys.exit(1)
       
        if still_running:
           log.error("Blockstackd appears to be running already.  If not, please run '{} stop'".format(sys.argv[0]))
           sys.exit(1)

        blockstack_backup_restore(working_dir, args.block_number)

        # make sure we're "stopped"
        set_indexing(working_dir, False)
        if os.path.exists(get_pidfile_path(working_dir)):
           os.unlink(get_pidfile_path(working_dir))

        # remember some recovery metadata the next time we start
        setup_recovery(working_dir)

    elif args.action == 'verifydb':
        expected_snapshots = None
        if args.expected_snapshots is not None:
           expected_snapshots = load_expected_snapshots(args.expected_snapshots)
           if expected_snapshots is None:
               sys.exit(1)
     
        tmpdir = tempfile.mkdtemp('blockstack-verify-chainstate-XXXXXX')
        rc = verify_database(args.consensus_hash, int(args.block_height), args.chainstate_dir, tmpdir, expected_snapshots=expected_snapshots)
        if rc:
           # success!
           print("Database is consistent with %s" % args.consensus_hash)
           print("Verified files are in '%s'" % working_dir)

        else:
           # failure!
           print("Database is NOT CONSISTENT")

    elif args.action == 'fast_sync_snapshot':
        # create a fast-sync snapshot from the last backup
        dest_path = str(args.path)
        private_key = str(args.private_key)
        try:
           keylib.ECPrivateKey(private_key)
        except:
           print("Invalid private key")
           sys.exit(1)

        block_height = None
        if args.block_height is not None:
           block_height = int(args.block_height)

        rc = fast_sync_snapshot(working_dir, dest_path, private_key, block_height)
        if not rc:
           print("Failed to create snapshot")
           sys.exit(1)

    elif args.action == 'fast_sync_sign':
        # sign an existing fast-sync snapshot with an additional key
        snapshot_path = str(args.path)
        private_key = str(args.private_key)
        try:
           keylib.ECPrivateKey(private_key)
        except:
           print("Invalid private key")
           sys.exit(1)

        rc = fast_sync_sign_snapshot( snapshot_path, private_key )
        if not rc:
           print("Failed to sign snapshot")
           sys.exit(1)

    elif args.action == 'fast_sync':
        # fetch the snapshot and verify it
        if hasattr(args, 'url') and args.url:
           url = str(args.url)
        else:
           url = str(config.FAST_SYNC_DEFAULT_URL)

        public_keys = config.FAST_SYNC_PUBLIC_KEYS

        if args.public_keys is not None:
           public_keys = args.public_keys.split(',')
           for pubk in public_keys:
               try:
                   keylib.ECPublicKey(pubk)
               except:
                   print("Invalid public key")
                   sys.exit(1)

        num_required = len(public_keys)
        if args.num_required:
           num_required = int(args.num_required)

        print("Synchronizing from snapshot from {}.  This may take up to 15 minutes.".format(url))

        rc = fast_sync_import(working_dir, url, public_keys=public_keys, num_required=num_required, verbose=True)
        if not rc:
           print('fast_sync failed')
           sys.exit(1)

        # treat this as a recovery
        setup_recovery(working_dir)

        print("Node synchronized!  Node state written to {}".format(working_dir))
        print("Start your node with `blockstack-core start`")
        print("Pass `--debug` for extra output.")

    elif args.action == 'audit':
        # audit the built-in genesis block 
        key_id = args.signing_key
        genesis_block_path = args.path

        res = do_genesis_block_audit(genesis_block_path=genesis_block_path, key_id=key_id)
        if not res:
            print('Genesis block is INVALID', file=sys.stderr)
            sys.exit(1)

        print('Genesis block is valid')
        sys.exit(0)