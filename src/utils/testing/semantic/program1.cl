class Main {
    step(p : AUTO_TYPE): Object { 
        p.translate(1,1) 
    };
    
    main() : Object {
        let p : AUTO_TYPE <- new Point in
            step(p)
    };
};