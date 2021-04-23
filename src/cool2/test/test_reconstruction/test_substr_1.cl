class Main
{
    main(): String
    {
        {
            s:String <- 
                "0123456789";
            s
            .substr(
                0,
                10
            )
            .concat(
                s
                .substr(
                    0,
                    5
                )
            )
            .concat(
                s
                .substr(
                    5,
                    5
                )
            );
        }
    };
}


